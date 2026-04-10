import pandas as pd
import os

# File path (update date if needed)
file_path = "data/trends_20240115.json"  # change to your actual file name

def main():
    # 1 — Load JSON file
    try:
        df = pd.read_json(file_path)
        print(f"Loaded {len(df)} stories from {file_path}")
    except Exception as e:
        print("Error loading JSON file:", e)
        return

    # 2 — Clean the Data

    # Remove duplicates based on post_id
    before = len(df)
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # Remove rows with missing values (post_id, title, score)
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # Convert data types
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # Remove low-quality stories (score < 5)
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # Remove extra whitespace in title
    df["title"] = df["title"].str.strip()

    # 3 — Save as CSV

    # Ensure data folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    output_file = "data/trends_clean.csv"
    df.to_csv(output_file, index=False)

    print(f"\nSaved {len(df)} rows to {output_file}")

    # Summary: stories per category
    print("\nStories per category:")
    print(df["category"].value_counts())


if __name__ == "__main__":
    main()