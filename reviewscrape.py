#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import argparse
import sys
import re
import json

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

    collected = []
    stop_flag = False

    for tag in soup.find_all(['p', 'h3']):
        if tag.name == 'h3':
            span = tag.find('span')
            if span and "latest updates to this best tvs guide" in span.text.lower():
                print("[INFO] Detected changelog heading. Halting scraping at this point.")
                break

        if tag.name == 'p':
            if tag.has_attr("class"):
                continue

            text = tag.get_text(strip=True)

            if len(text) >= 200 and "Matt" not in text:
                collected.append(text)

    if not collected:
        print("[INFO] No suitable paragraphs found.")
    else:
        print(f"[INFO] Found {len(collected)} usable paragraphs.")
        for i, para in enumerate(collected, 1):
            print(f"\n[{i}] {para}\n")

        with open("output_techradar.jsonl", "w", encoding="utf-8") as f:
            for para in collected:
                f.write(json.dumps({
                    "instruction": "Write a product review based on the provided notes.",
                    "input": para,
                    "output": ""
                }) + "\n")

        print("[INFO] Exported to output_techradar.jsonl")

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
