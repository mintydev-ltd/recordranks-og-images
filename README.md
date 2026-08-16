# RecordRanks OG Images

Microservice that generates Open Graph image previews for a RecordRanks instance. It launches a headless Chromium browser via Playwright, navigates to the requested page, and returns a 1200x630 JPEG screenshot. Results are cached in memory.

## Configuration

The configuration is just a `.env` file:

| Variable             | Description                                   | Example               |
| -------------------- | --------------------------------------------- | --------------------- |
| `PRODUCTION_APP_URL` | URL of the RecordRanks instance to screenshot | `https://example.com` |

## Docker

Build and run it with Docker. In production, you can run it using the existing RecordRanks Kubernetes setup.

```bash
docker build -t recordranks-og-images .

docker run --rm -p 3050:80 -e PRODUCTION_APP_URL=https://example.com recordranks-og-images
```

The service itself listens on port `80` (though it's exposed on port `3050` above). It simply takes the full path of the page you want to get an image preview of, and then returns an image blob. It only accepts public RecordRanks pages (e.g. competitions, rankings, records, etc.). The space ID parameter is required, even for instances with multi-tenancy disabled. You should host this service under a subdomain (e.g. `og-images.example.com`), with your proxy forwarding requests to the Docker container/Kubernetes pod.

## Example

To get an image preview of `https://example.com/default/competitions`, send a `GET` request to:

```
https://og-images.example.com/default/competitions
```
