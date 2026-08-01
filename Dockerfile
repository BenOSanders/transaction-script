# syntax=docker/dockerfile:1

FROM python:3.14-slim
WORKDIR /app
COPY . .
USER nonroot
CMD ["uv", "run", "fastapi", "run"]
