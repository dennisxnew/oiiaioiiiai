# Use official Python image
FROM python:3.11-slim

# Set the parent directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Create the backend directory
RUN mkdir backend

# Copy dependency files
COPY pyproject.toml poetry.lock* ./backend/

# Set WORKDIR to the backend directory
WORKDIR /app/backend

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root --only main

# Copy the rest of the application source code
COPY . .

# Set the Python Path to the parent directory /app
# This ensures that `from backend.src...` imports work correctly
ENV PYTHONPATH=/app

# Expose the port
EXPOSE 8080

# Command to run the application
# uvicorn runs from WORKDIR (/app/backend), so it finds `src.main:app`
# The app's code finds `backend` via PYTHONPATH=/app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]