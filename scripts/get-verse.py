#!/usr/bin/env python3
import urllib.request
import re

def fetch_verse():
    url = "https://www.bible.com/verse-of-the-day"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
            # Look for image alt text: <img alt="Ephesians 4:2 - Be completely humble..."
            match = re.search(r'<img\s+alt="([^"]+?\s+-\s+[^"]+?)"', html)
            if match:
                alt_text = match.group(1)
                # Split at ' - '
                if ' - ' in alt_text:
                    ref, text = alt_text.split(' - ', 1)
                    return f"“{text.strip()}” — {ref.strip()}"
    except Exception:
        pass

    # Fallback to OurManna
    try:
        import json
        url_fb = "https://beta.ourmanna.com/api/v1/get?format=json&order=daily"
        req_fb = urllib.request.Request(url_fb, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_fb, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            details = data['verse']['details']
            return f"“{details['text'].strip()}” — {details['reference']}"
    except Exception:
        return "Unable to fetch verse"

if __name__ == "__main__":
    print(fetch_verse())