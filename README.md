# Daily AI & Tech News Digest

This project sends a daily email summarizing the latest news in artificial intelligence and technology. It uses the NewsAPI service to collect top headlines and formats them into an HTML email.

## Features

- Pulls top AI/tech news from the previous day
- Formats a clean HTML summary with clickable links
- Sends the email to one or more recipients
- Fully configurable via `.env` file
- Optional scheduling for 6:00 AM daily delivery

## Prerequisites

- Python 3.x
- Gmail account with App Password enabled
- A free NewsAPI key from https://newsapi.org

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Dhruvptl17/newsletter_project.git
cd newsletter_project
