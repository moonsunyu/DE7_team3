# API_KEY = "633b071420476eea43525a6747c22e0c"

import pandas as pd
import requests
import time

# -------------------------
# CONFIG
# -------------------------
API_KEY = "633b071420476eea43525a6747c22e0c"
INPUT_FILE = "restaurants_all_pages.csv"
OUTPUT_FILE = "restaurants_with_info.csv"
STILL_SKIPPED_FILE = "restaurants_still_skipped.csv"

SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"
HEADERS = {"Authorization": f"KakaoAK {API_KEY}"}

# -------------------------
# READ CSV
# -------------------------
df = pd.read_csv(INPUT_FILE)

matched_rows = []
skipped_rows = []

# -------------------------
# FUNCTION TO SEARCH KAKAO
# -------------------------
def search_kakao(query, lat=None, lng=None, radius=800, size=20):
    params = {
        'query': query,
        'size': size,
        'category_group_code': 'FD6'
    }
    if lat and lng:
        params.update({'x': lng, 'y': lat, 'radius': radius})
    try:
        res = requests.get(SEARCH_URL, headers=HEADERS, params=params, timeout=5)
        res.raise_for_status()
        return res.json().get('documents', [])
    except requests.exceptions.RequestException as e:
        print("API error:", e)
        return []

# -------------------------
# LOOP THROUGH RESTAURANTS
# -------------------------
for idx, row in df.iterrows():
    lat, lng = row.get('latitude'), row.get('longitude')
    restaurant_name = row.get('name') or row.get('상호명')
    
    if not lat or not lng:
        skipped_rows.append(row)
        continue

    # Search by coordinates + generic keyword (nearest restaurant)
    docs = search_kakao("음식점", lat, lng, radius=800, size=1)
    matched_place = docs[0] if docs else None

    # Optional fallback: stricter name match
    if matched_place and restaurant_name:
        if restaurant_name not in matched_place.get("place_name", ""):
            # fallback: search by name only
            docs_name_only = search_kakao(restaurant_name, size=5)
            matched_place = docs_name_only[0] if docs_name_only else matched_place

    # -------------------------
    # SAVE RESULTS
    # -------------------------
    if matched_place:
        place_id = matched_place.get("id")
        kakao_url = f"https://place.map.kakao.com/{place_id}"
        matched_rows.append({
            '상호명': matched_place.get("place_name", ""),
            '주소': matched_place.get("road_address_name") or matched_place.get("address_name", ""),
            '전화번호': matched_place.get("phone", ""),
            '메뉴': matched_place.get("menu", ""),
            '카카오맵URL': kakao_url,
            '카카오맵ID': place_id or ""
        })
        print(f"[{idx+1}/{len(df)}] Matched: {matched_place.get('place_name')}")
    else:
        skipped_rows.append(row)
        print(f"[{idx+1}/{len(df)}] No match found")

    time.sleep(0.3)  # prevent rate limiting

# -------------------------
# SAVE CSV
# -------------------------
pd.DataFrame(matched_rows).to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
if skipped_rows:
    pd.DataFrame(skipped_rows).to_csv(STILL_SKIPPED_FILE, index=False, encoding='utf-8-sig')

print("Done!")
print("Matched saved to:", OUTPUT_FILE)
print("Still skipped saved to:", STILL_SKIPPED_FILE)
