# 🕷️ Web-Scrape-Notifier

This Web-Scrape-Notifier is a lightweight, configuration based web scraper developed for the purpose of monitoring webpages for inventory restocks or content changes. Originally built to report Raspberry Pi restocks for building out my homelab, I've refactored it to function in a Docker Container. By customizing the configuration file with a target URL and HTML element, this utility will monitor the target webpage on a defined schedule to dispatch an email or SMS text alerts as soon as a change is detected.
  
## 📂 Project Structure

```
/Web-Scrape-Notifier
├── .env.example        # Environment variable example
├── compose.yaml        # Docker container orchestration
├── config.json         # User selected URLs and HTML element selectors
├── Dockerfile          # Container build instructions
├── message.py          # Email/SMS notification script
├── requirements.txt    # Python library dependencies
└── scrape.py           # Web-scraping script
```

## 🚀 Getting Started

1. Clone the repository using: `git clone https://github.com/cdmanning/Web-Scrape-Notifier.git`

2. Ensure you have [Docker](https://docs.docker.com/get-started/get-docker/) and [Docker Compose](https://docs.docker.com/compose/) installed on your system.

3. Rename the .env.example file to .env in the root directory.

    ### Setting up your `.env` File
    - SMTP_USER: The email address the script will use to send alerts.
    - SMTP_PASSWORD: Your email's app password.
    - SMTP_SERVER: The outgoing mail server for your email provider.
    - SMTP_PORT: The port your mail server uses for communication.
    - RECIPIENT_EMAIL: The destination address for the alert (see the SMS section below for texting).
    - CRON_SCHEDULE: The interval at which the script runs.

4. Start the container by running: 
```bash
docker compose -f compose.yaml up  -d
```


## ⚙️ Configuration

### 📱 Sending Texts via SMS Gateways
Using the standard SMTP communication protocol this script can easily be configured to send text messages directly to your phone. Most mobile carriers have a SMS-to-Email gateway which can be used to achieve this outcome.

- T-Mobile: `phone_number@tmomail.net`

- Verizon: `phone_number@vtext.com`

- AT&T: `phone_number@txt.att.net`


### ⏱️ Setting Timers with Cron
This docker project uses Linux CRON jobs to orchestrate its scheduling. You can adjust the CRON_SCHEDULE variable in your .env file using standard cron syntax:
- `*/10 * * * *` - Runs every 10 minutes.

- `0 * * * *` - Runs at the start of every hour.

- `0 8,20 * * *` - Runs twice a day at 8:00 AM and 8:00 PM.

### 🎯 Configuring the JSON Configuration
To start monitoring a website for changes add a new entry to the `config.json` define your target. The script detects changes by looking at a specific HTML tag and class, checking if your defined target text is missing. 
```
{
  "name": "Example Online Website",
  "url": "https://www.example.com/product",
  "element_tag": "div",
  "element_class": "inventory-status",
  "target_text": "Sold Out"
}
```
If the exact target_text (e.g., "Sold Out") is not found within the `<div class="inventory-status">` container on the webpage, the script assumes a change has occurred and will trigger an alert.

### 🧪 Updating and Testing
When making changes to `config.json`, you do not need to restart the container. Simply edit the file on your filesystem, and the updates will automatically be picked up on the next scheduled cron job cycle. 

To test your configuration or trigger a check immediately without waiting for the timer, you can execute the script manually inside the running container by running:

```bash
docker exec Web-Scrape-Notifier python scrape.py
```
