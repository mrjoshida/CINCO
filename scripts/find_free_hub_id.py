#!/usr/bin/env python3
"""Query the live catalog from The Firmware Hub to identify taken firmware identities

and find a confirmed 100% unique, unassigned identity for Cinco.
"""

import json
import re
import sys
import urllib.error
import urllib.request

CANDIDATES = [
    "FM-1_555",
    "FM-1_4343",
    "FM-1_25",
    "FM-1_250",
    "FM-1_728",
    "FM-1_9025",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
}


def fetch_url(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            return content.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code} fetching {url}: {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def extract_from_json(obj, taken_ids, raw_matches):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() in ("id", "identity", "product", "product_id", "fw_id", "package_id", "model"):
                if isinstance(v, str):
                    taken_ids.add(v)
            extract_from_json(v, taken_ids, raw_matches)
    elif isinstance(obj, list):
        for item in obj:
            extract_from_json(item, taken_ids, raw_matches)


def main():
    catalog_url = "https://thefirmwarehub.com/catalog.json"
    print(f"Fetching catalog from {catalog_url}...")
    catalog_raw = fetch_url(catalog_url)
    if not catalog_raw:
        print("Failed to fetch catalog.json!", file=sys.stderr)
        sys.exit(1)

    taken_ids = set()
    raw_matches = set()

    # Parse JSON
    try:
        catalog_data = json.loads(catalog_raw)
        extract_from_json(catalog_data, taken_ids, raw_matches)
        print(f"Catalog JSON successfully parsed. Top-level keys: {list(catalog_data.keys()) if isinstance(catalog_data, dict) else len(catalog_data)}")
    except Exception as e:
        print(f"Failed to parse catalog JSON: {e}")

    # Regex search across raw catalog text for any FM-1_ patterns or variations
    fm1_all = set(re.findall(r"FM-1_[A-Za-z0-9_-]+", catalog_raw))
    print(f"Found {len(fm1_all)} regex matches of 'FM-1_*' in raw catalog.json")
    taken_ids.update(fm1_all)

    # Also check if any candidate appears anywhere in the raw catalog text (substring search)
    print("\n--- All known taken FM-1 identities found in catalog.json ---")
    for tid in sorted(fm1_all):
        print(f"  - {tid}")

    # Check for "SLOOP" in catalog
    sloop_entries = []
    if isinstance(catalog_data, dict) and "firmwares" in catalog_data:
        for fw in catalog_data["firmwares"]:
            if "sloop" in fw.get("id", "").lower() or "sloop" in fw.get("name", "").lower():
                sloop_entries.append(fw)
    print(f"\nSLOOP entries in firmwares ({len(sloop_entries)}):")
    for se in sloop_entries:
        print(f"  id: {se.get('id')}, name: {se.get('name')}, pkg: {se.get('pkg')}, release: {se.get('release')}")
        if "product" in se or "identity" in se:
            print(f"    product/identity: {se.get('product') or se.get('identity')}")


    # Also check https://thefirmwarehub.com/kb/ or related endpoints
    kb_url = "https://thefirmwarehub.com/kb/"
    print(f"\nChecking KB at {kb_url}...")
    kb_raw = fetch_url(kb_url)
    if kb_raw:
        kb_fm1 = set(re.findall(r"FM-1_[A-Za-z0-9_-]+", kb_raw))
        print(f"Found {len(kb_fm1)} regex matches of 'FM-1_*' in KB")
        taken_ids.update(kb_fm1)

    print("\n--- Complete Set of Taken IDs / Products ---")
    for tid in sorted(taken_ids):
        if "FM-1" in tid or tid.isdigit():
            print(f"  {tid}")

    print("\n--- Detailed Deep Check of Candidates ---")
    for cand in CANDIDATES:
        cand_in_raw = cand in catalog_raw
        num_part = cand.split("_")[1]
        matches = [m for m in fm1_all if num_part in m]
        print(f"{cand}: in_raw={cand_in_raw}, any_partial_matches_in_catalog={matches}")



if __name__ == "__main__":
    main()
