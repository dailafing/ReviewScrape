# Menu

- Project Breifing - <b>You are here</b>
- <a href="docs/TESTING.md">Application Testing </a>
---

# ReviewScraper - Project Breifing

ReviewScraper is designed to take an input URL for a website that contains product reviews, and collect the information to be stored as JSON data. Do not use it unless you have the explicit permission from the IP owner, and always follow and respect the law.

----

### Installation & Enviroment

#### For macOS/Linux:
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

#### For Windows (PowerShell:
python -m venv .venv ; .\.venv\Scripts\Activate.ps1 ; pip install -r requirements.txt
)

----

### Example Usage

#### For macOS/Linux:
python3 reviewscrape.py -url https://www.techradar.com/uk/news/best-tv
