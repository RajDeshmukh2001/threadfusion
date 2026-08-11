# Use lightweight Python 3.11 as the base image
FROM python:3.11-slim

WORKDIR /app

# Don't create .pyc cache files (keeps container clean)
ENV PYTHONDONTWRITEBYTECODE=1
# Show Python logs immediately (helps with debugging)
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

# Install all Python packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Make entrypoint.sh executable
RUN chmod +x entrypoint.sh

EXPOSE 8000

# Use entrypoint.sh as the startup command
ENTRYPOINT ["./entrypoint.sh"]