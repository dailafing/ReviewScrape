#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import argparse
import sys
import re
import json
import os
import time

MIN_PARAGRAPH_LENGTH = 200
OUTPUT_PATH = "output_data.jsonl"
DESTINATION_NAME = "ReviewCave.co.uk"

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
    current_heading = None

    stop_keywords = [
        "writes for", "freelance", "journalist", "Alistair", "contributor",
        "editorial", "byline", "tech enthusiast", "writes about", "worked as", "coverage for",
        "Matt", "Harry", "He enjoys", "Jamie", "Tom Power", "Abigail", "Mike"
    ]

    for tag in soup.find_all(['h2', 'h3', 'p']):
        # STOP parsing at changelog section
        if tag.name == 'h3':
            span = tag.find('span')
            if span and "latest updates to this best tvs guide" in span.text.lower():
                print("[INFO] Detected changelog heading. Halting scraping at this point.")
                break

        # Track current heading context
        if tag.name == 'h2':
            current_heading = tag.get_text(separator=" ", strip=True)
            continue

        # Process paragraph content
        if tag.name == 'p':
            if tag.has_attr("class"):
                continue

            # Fix <br> tag spacing
            for br in tag.find_all("br"):
                br.replace_with(". ")

            text = tag.get_text(separator=" ", strip=True)

            if any(kw.lower() in text.lower() for kw in stop_keywords):
                continue

            if len(text) >= MIN_PARAGRAPH_LENGTH:
                text = sanitize_brands(text)
                collected.append({
                    "context": current_heading or "",
                    "input": text
                })

    saveToJSON(collected)


def saveToJSON(collected):
    existing_inputs = set()

    # Load existing data for deduplication
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    existing_inputs.add(obj.get("input", "").strip())
                except json.JSONDecodeError:
                    continue

    new_entries = []
    for item in collected:
        text = item["input"].strip()
        if text not in existing_inputs:
            new_entries.append({
                "instruction": "Write a product review based on the provided notes.",
                "context": item["context"].strip(),
                "input": text,
                "output": ""
            })

    if not new_entries:
        print("[INFO] No new unique paragraphs to add.")
    else:
        print(f"[INFO] Adding {len(new_entries)} new unique paragraphs.")
        with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
            for entry in new_entries:
                f.write(json.dumps(entry) + "\n")

        print(f"[INFO] Appended to {OUTPUT_PATH}")
    

def sanitize_brands(text):
    """
    Replace all known brand mentions with DESTINATION_NAME.
    Case-insensitive, safe for inline text, and avoids partial word matches.
    """
    brands_to_replace = [
        "TechRadar",  # Add more brands here later: "Wired", "Forbes", etc.
    ]

    for brand in brands_to_replace:
        pattern = re.compile(rf"\b{re.escape(brand)}\b", flags=re.IGNORECASE)
        text = pattern.sub(DESTINATION_NAME, text)

    return text


def main():
    parser = argparse.ArgumentParser(description="Scrape structured review content from known domains.")
    parser.add_argument('-url', '--url', type=str, help='URL of a single review article to scrape')
    parser.add_argument('-list', '--list', type=str, help='Path to a .txt file with URLs to scrape')
    args = parser.parse_args()

    urls = []

    if args.list:
        list_path = args.list.strip()
        if not os.path.exists(list_path):
            print(f"[ERROR] List file not found: {list_path}")
            sys.exit(1)

        with open(list_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    urls.append(line)

    elif args.url:
        urls.append(args.url.strip())
    else:
        url = input("Enter the URL of the review page: ").strip()
        urls.append(url)

    for i, url in enumerate(urls):
        domain = extract_domain(url)
        print(f"\n[INFO] ({i+1}/{len(urls)}) Scraping: {url}")
        print(f"[INFO] Detected domain: {domain}")

        if "techradar.com" in domain:
            scrape_techradar(url)
        else:
            print(f"[ERROR] Unsupported domain: {domain}")
            print("Currently supported domains: techradar.com")

        if i < len(urls) - 1:
            print("[INFO] Pausing for 2 seconds before next URL...")
            time.sleep(2)

        

if __name__ == '__main__':
    main()
