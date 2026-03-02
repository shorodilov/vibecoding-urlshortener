# Reference URL Shortener -- demo service by vibe coding

> [!IMPORTANT]
> This is an experimental repository created for educational purposes.
> It is not intended for production use.

This is demo AI-assisted URL shortener project.

## Service

A simple URL shortener with three endpoints:

| Method | URL Path        | Description                                 |
|--------|-----------------|---------------------------------------------|
| `POST` | `/shorten`      | Accept a long URL, and return a short code. |
| `GET`  | `/{code}`       | Redirect to the original URL.               |
| `GET`  | `/stats/{code}` | Return redirect count for the code.         |

## Running locally

[uv]: https://docs.astral.sh/uv/

**Prerequisites**:
* Python3.12+
* [uv][uv]

To install dependencies run command in your terminal:

```shell
uv sync
```
