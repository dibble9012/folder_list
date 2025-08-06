import requests
import re
import time

API_KEY = "KEY HERE"
INPUT_FILE = "Movie_List.txt"
OUTPUT_FILE = "Movie_List_With_Years.txt"

def get_movie_year(title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": API_KEY,
        "query": title,
        "include_adult": "true"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            release_date = results[0].get("release_date", "")
            if release_date:
                return release_date[:4]
    return None

with open(INPUT_FILE, "r") as f:
    movie_titles = [line.strip() for line in f if line.strip()]

updated_list = []
for idx, title in enumerate(movie_titles):
    clean_title = re.sub(r"\s*\(.*?\)", "", title)  # Strip parenthetical content
    year = get_movie_year(clean_title)
    final_title = f"{clean_title} ({year})" if year else f"{clean_title} (YEAR NOT FOUND)"
    updated_list.append(final_title)
    print(f"{idx + 1}/{len(movie_titles)}: {final_title}")
    time.sleep(0.25)  # Avoid API rate limits

with open(OUTPUT_FILE, "w") as f:
    f.writelines(f"{line}\n" for line in updated_list)

print(f"\n✅ Done! Output saved to: {OUTPUT_FILE}")
