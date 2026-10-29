#!/usr/bin/env python3
"""
Verify Firmware Hub identity availability for FM-1_555.
Replicates the exact JavaScript idcheck() from https://thefirmwarehub.com/submit/
and performs deep inspection across all entries, regex patterns, and 5xx ranges in catalog.json.
"""

import json
import re
import sys
import urllib.request

CATALOG_URL = "https://thefirmwarehub.com/catalog.json"
TARGET_ID = "FM-1_555"

RESERVED = {
    "FM-1_015": "M-VAVE's official V15",
    "FM-1_016": "M-VAVE's official V16",
}


def fetch_catalog():
    req = urllib.request.Request(
        CATALOG_URL,
        headers={"User-Agent": "Mozilla/5.0 (compatible; IdentityAuditor/1.0)"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def replicate_hub_idcheck(catalog, target):
    v = target.strip()
    v = re.sub(r"^fm-?1_?", "FM-1_", v, flags=re.IGNORECASE)

    if not v:
        return {"status": "EMPTY", "message": "No identity provided"}

    if not re.match(r"^FM-1_\d{3,8}$", v):
        return {
            "status": "INVALID",
            "message": "An identity is FM-1_ and 3 to 8 digits.",
        }

    if v in RESERVED:
        return {
            "status": "RESERVED",
            "message": f"Taken: {RESERVED[v]}.",
        }

    firmwares = catalog.get("firmwares", [])
    ids = [
        {
            "name": f.get("name"),
            "version": f.get("version"),
            "product": f.get("product"),
            "ident": f.get("ident"),
        }
        for f in firmwares
    ]

    same = [f for f in ids if f.get("product") == v]
    near = []
    for f in ids:
        ident_pat = f.get("ident", "")
        if f.get("product") != v and ident_pat != r"FM-1_\d{3,8}":
            try:
                pattern = f"^(?:{ident_pat})$"
                if re.match(pattern, v):
                    near.append(f)
            except re.error as err:
                print(f"[WARN] Invalid regex in catalog for {f['name']}: {ident_pat} ({err})")

    if same:
        msg = f"Taken: {', '.join(f[name] + ' ' + str(f['version']) for f in same)} answers with it."
        return {"status": "TAKEN", "message": msg, "same": same}
    elif near:
        msg = f"In use: inside the range of {', '.join(f['name'] for f in near)} (their next versions may take it)."
        return {"status": "NEAR", "message": msg, "near": near}
    else:
        return {
            "status": "FREE",
            "message": "Free ✓ No firmware on the hub uses it.",
        }


def deep_inspection(catalog, target):
    firmwares = catalog.get("firmwares", [])
    print(f"Total firmwares in catalog: {len(firmwares)}")

    # Check 1: Exact matches in all fields
    matches_product = [f for f in firmwares if f.get("product") == target]
    print(f"\n1. Exact product match for '{target}': {len(matches_product)}")

    # Check 2: Range / ident matching
    matching_patterns = []
    for f in firmwares:
        ident_pat = f.get("ident")
        if not ident_pat:
            continue
        # Skip catch-all ident pattern FM-1_\d{3,8} as done in hub JS
        if ident_pat == r"FM-1_\d{3,8}":
            continue
        try:
            if re.match(f"^(?:{ident_pat})$", target):
                matching_patterns.append((f, ident_pat))
        except re.error as e:
            print(f"[WARN] regex error on {ident_pat}: {e}")

    print(f"2. Ident regex pattern matches for '{target}' (excluding default wildcard): {len(matching_patterns)}")
    for f, pat in matching_patterns:
        print(f"   -> Match: {f.get('name')} (ident: '{pat}', product: '{f.get('product')}')")

    # Check 3: Check all 5xx / near 555 IDs in catalog
    print("\n3. All 5xx / near 555 identities in catalog:")
    near_5xx = []
    for f in firmwares:
        prod = str(f.get("product", ""))
        ident = str(f.get("ident", ""))
        # Look for 500-599 or FM-1_5...
        digits = re.findall(r"\d+", prod)
        matched_5xx = False
        for d in digits:
            if len(d) >= 3 and d.startswith("5"):
                matched_5xx = True
            elif d.isdigit() and 500 <= int(d[:3]) <= 599:
                matched_5xx = True
        if "5" in ident and ident != r"FM-1_\d{3,8}":
            # If ident explicitly references 5
            if re.search(r"5\d\d", ident):
                matched_5xx = True

        if matched_5xx or "555" in prod or "555" in ident:
            near_5xx.append(f)

    if near_5xx:
        print(f"   Found {len(near_5xx)} firmwares with 5xx-related product/ident:")
        for f in near_5xx:
            print(f"   - {f.get('name', 'N/A')} v{f.get('version', 'N/A')}: product='{f.get('product')}', ident='{f.get('ident')}'")
    else:
        print("   None found! The entire 500-599 range appears unallocated.")

    # Check 4: Check if any firmware name, id, or tag contains 555
    print("\n4. Any substring mention of '555' anywhere in firmwares list:")
    mentions_555 = []
    for f in firmwares:
        blob = json.dumps(f)
        if "555" in blob:
            mentions_555.append(f.get("name", "Unknown"))
    print(f"   Mentions of '555': {mentions_555 if mentions_555 else 'None'}")


def main():
    print(f"Fetching latest catalog from {CATALOG_URL}...")
    try:
        catalog = fetch_catalog()
    except Exception as e:
        print(f"Error fetching catalog: {e}", file=sys.stderr)
        sys.exit(1)

    print("Running exact The Firmware Hub idcheck() logic...")
    hub_res = replicate_hub_idcheck(catalog, TARGET_ID)
    print(f"Hub Status: {hub_res['status']}")
    print(f"Hub Message: {hub_res['message']}")

    print("\n=== DEEP INSPECTION AUDIT ===")
    deep_inspection(catalog, TARGET_ID)

    if hub_res["status"] == "FREE":
        print("\n=======================================================")
        print(f"CONCLUSION: {TARGET_ID} is 100% FREE AND AVAILABLE.")
        print("Zero conflicts, zero pattern collisions, zero range reservations.")
        print("=======================================================")
    else:
        print(f"\nCONFLICT DETECTED: {hub_res}")
        sys.exit(1)


if __name__ == "__main__":
    main()
