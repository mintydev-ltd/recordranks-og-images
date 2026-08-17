# RecordRanks OG Images

Microservice that generates Open Graph image previews for a RecordRanks instance. It launches a headless Chromium browser via Playwright, navigates to the requested page, and returns a 1200x630 JPEG screenshot. Results are cached in memory.

## Configuration

The configuration is just a `.env` file:

| Variable             | Description                                   | Example               |
| -------------------- | --------------------------------------------- | --------------------- |
| `PRODUCTION_APP_URL` | URL of the RecordRanks instance to screenshot | `https://example.com` |

## Docker

Build it with Docker and run it with Kubernetes in production, using the `start-prod.sh` script.

```bash
docker build -t recordranks-og-images .

./start-prod.sh
```

The container itself listens on port `80`, but the K8s service exposes it on port `31050`. It simply takes the full path of the page you want to get an image preview of, and then returns an image blob. It only accepts public RecordRanks pages (e.g. competitions, rankings, records, etc.). The space ID parameter is required, even for instances with multi-tenancy disabled. You should host this service under a subdomain (e.g. `og-images.example.com`), with your proxy forwarding requests to the Kubernetes service.

## Example

To get an image preview of `https://example.com/default/competitions`, send a `GET` request to:

```
https://og-images.example.com/default/competitions
```
