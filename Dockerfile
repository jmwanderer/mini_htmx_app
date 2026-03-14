FROM python:3.13-slim

WORKDIR /app

# Install app dependencies
COPY  requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

ENV PORT=8080

CMD gunicorn contactsdb:app \
    --bind 0.0.0.0:${PORT}

