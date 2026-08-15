from fastapi import FastAPI, Request, Response
from urllib.parse import urlencode
from playwright.async_api import async_playwright
from aiocache import SimpleMemoryCache
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging
import re

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env") # only used in dev
    prod_hostname: str
    multitenancy_enabled: bool

app = FastAPI()
settings = Settings()
cache = SimpleMemoryCache()
logger = logging.getLogger(__name__)

CACHE_TTL = 3600  # 1 hour

@app.get("/{path:path}")
async def read_root(request: Request, path: str):
    # Regex taken from https://github.com/mintydev789/RecordRanks/blob/main/client/proxy.ts
    if ((settings.multitenancy_enabled
            and not re.match(r'^[^/]+(\/|\/(about|competitions|export|moderator-instructions|blog|rankings|records|rules|video-based-results)(\/.*)?)?$', path))
        or (not settings.multitenancy_enabled
            and not re.match(r'^(about|competitions|export|moderator-instructions|blog|rankings|records|rules|video-based-results)(\/.*)?$', path))):
        return Response(
            content=f"Error: Unsupported path: {path}",
            media_type="text/plain",
            status_code=400,
        )

    # Reconstruct the full URL
    query_params = dict(request.query_params)
    target_url = f"https://{settings.prod_hostname}/{path}"

    if query_params:
        target_url += f"?{urlencode(query_params)}"

    cached = await cache.get(target_url)
    if cached is not None:
        return Response(content=cached, media_type="image/jpeg")

    logger.info("Creating screenshot for: %s", target_url)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # Set viewport for OG image dimensions
        await page.set_viewport_size({"width": 1200, "height": 630})
        await page.goto(target_url)
        await page.wait_for_selector("#loading_spinner", state="hidden", timeout=5000)
        # Scroll to the #main element
        await page.evaluate('document.querySelector("main")?.scrollIntoView({ behavior: "instant" });')

        image_bytes = await page.screenshot(type="jpeg", quality=85, full_page=False)
        await browser.close()

    await cache.set(target_url, image_bytes, ttl=CACHE_TTL)

    return Response(content=image_bytes, media_type="image/jpeg")
