#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import argparse
import sys

MIN_PARAGRAPH_LENGTH = 200

def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc.lower().replace("www.", "")

def scrape_techradar(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Failed to retrieve the page: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')

    all_paragraphs = soup.find_all("p")
    extracted = []

    for p in all_paragraphs:
        # Only include <p> tags with no class attribute
        if not p.has_attr("class"):
            text = p.get_text(strip=True)
            if len(text) >= MIN_PARAGRAPH_LENGTH:
                extracted.append(text)

    if not extracted:
        print("[INFO] No suitable paragraphs found.")
    else:
        print("\n[INFO] Extracted Paragraphs:\n")
        for i, para in enumerate(extracted, 1):
            print(f"{'-'*40}\n[{i}] {para}\n")

def main():
    parser = argparse.ArgumentParser(description="Scrape structured review content from known domains.")
    parser.add_argument('-url', '--url', type=str, help='URL of the review article to scrape')
    args = parser.parse_args()

    url = args.url
    if not url:
        url = input("Enter the URL of the review page: ").strip()

    domain = extract_domain(url)

    print(f"[INFO] Detected domain: {domain}")

    if "techradar.com" in domain:
        scrape_techradar(url)
    else:
        print(f"[ERROR] Unsupported domain: {domain}")
        print("Currently supported domains: techradar.com")
        sys.exit(1)

if __name__ == '__main__':
    main()
