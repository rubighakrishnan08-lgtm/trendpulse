import requests
import time
import json
import os
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header (as required)
headers = {"User-Agent": "TrendPulse/1.0"}

# Category keywords (case-insensitive)
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Function to assign category based on title
def assign_category(title):
    title_lower = title.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None


def main():
    collected_data = []
    category_count = {cat: 0 for cat in categories}

    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        story_ids = response.json()[:500]  # First 500 IDs
    except Exception as e:
        print("Failed to fetch top stories:", e)
        return

    # Loop through categories
    for category in categories:
        print(f"\nCollecting {category} stories...")

        for story_id in story_ids:
            if category_count[category] >= 25:
                break

            try:
                res = requests.get(ITEM_URL.format(story_id), headers=headers)
                story = res.json()
            except Exception as e:
                print(f"Error fetching story {story_id}: {e}")
                continue

            # Skip invalid stories
            if not story or "title" not in story:
                continue

            title = story.get("title", "")

            # Check category match
            assigned = assign_category(title)

            if assigned == category:
                data = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                collected_data.append(data)
                category_count[category] += 1

        # Sleep AFTER each category (important requirement)
        time.sleep(2)

    # Create data folder if not exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # File name with date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Save JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    print(f"\nCollected {len(collected_data)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()