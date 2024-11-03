# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install Poetry and dependencies
RUN pip install --no-cache poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root

# Copy the rest of the application code
COPY ./src /app/src

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
