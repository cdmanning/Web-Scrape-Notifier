# Lightweight Python environment using Alpine Linux
FROM python:3.11-alpine

# Set the Working directory
WORKDIR /app

# Install gettext
RUN apk add --no-cache gettext

# Copy and install requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create cron template file
RUN echo '${CRON_SCHEDULE} cd /app && /usr/local/bin/python scrape.py >> /proc/1/fd/1 2>&1' > /etc/crontabs/cron_template

# Write to root and start cron job
CMD ["/bin/sh", "-c", "envsubst < /etc/crontabs/cron_template > /etc/crontabs/root && exec crond -f -d 8"]