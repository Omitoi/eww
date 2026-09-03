#!/usr/bin/env python3
import urllib.request
import re
import json

def fetch_verse():
    # 1. Primary: YouVersion Bible.com Daily Verse
    try:
        url = "https://www.bible.com/verse-of-the-day"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8')
            match = re.search(r'<img\s+alt="([^"]+?\s+-\s+[^"]+?)"', html)
            if match:
                alt_text = match.group(1)
                if ' - ' in alt_text:
                    ref, text = alt_text.split(' - ', 1)
                    clean_text = " ".join(text.split())
                    clean_ref = " ".join(ref.split())
                    return f"“{clean_text}” — {clean_ref}"
    except Exception:
        pass

    # 2. Secondary Fallback: OurManna API
    try:
        url = "https://beta.ourmanna.com/api/v1/get?format=json&order=daily"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            details = data['verse']['details']
            clean_text = " ".join(details['text'].split())
            clean_ref = " ".join(details['reference'].split())
            return f"“{clean_text}” — {clean_ref}"
    except Exception:
        pass


    return "Unable to fetch verse"

if __name__ == "__main__":
    print(fetch_verse())