FROM python:3.13-slim

WORKDIR /app

# Install app dependencies
COPY  requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

ENV DB_PATH=${WORKDIR}

CMD [ "gunicorn", "--workers=2",  "--bind",  "0.0.0.0:8080", "contactsdb:app" ]

