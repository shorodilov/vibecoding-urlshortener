# Reference URL Shortener Service -- Specification

> [!IMPORTANT]
> This document is intentionally not a production specification.
> Its goal is to provide a realistic but bounded context.
> Any elaboration must be justified by its educational value.

## Tech Stack

* Python 3.12
* uv
* FastAPI
* PostgreSQL

## Code layout

Project follows the `src` layout:

```
src/
  app/        # application package
tests/
migrations/
```

## Endpoints

### `POST /shorten`

Register the given URL and assign a shortcut for it.

Request body:
```json
{ "url": "https://example.com/very/long/path" }
```

Response `HTTP 201 Created`:
```json
{ "code": "abcd1234", "short_url": "http://example.com/abcd1234" }
```

### `GET /{code}`

Redirect to the original URL.
Response `HTTP 302 Found`, or `HTTP 404 Not Found` if code does not exist.

### `GET /stats/{code}`

Return a redirect count for the code.

Response `HTTP 200 OK`:
```json
{ "code": "abcd1234", "redirect_count": 42 }
```

Response `HTTP 404 Not Found` if code does not exist.

## Expectations

* Redirect path must have low latency; shorten may be slower.
