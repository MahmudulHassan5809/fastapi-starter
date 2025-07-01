FROM python:3.12-slim
RUN apt-get update && \
    apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh
WORKDIR /app
COPY . .
ENV PATH="/root/.local/bin/:$PATH"
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
RUN uv sync
EXPOSE 8000
