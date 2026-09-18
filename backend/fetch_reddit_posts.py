"""Fetch posts from academic-integrity-related subreddits and store them.

Uses Reddit's public per-subreddit `.json` listing endpoints (e.g.
https://www.reddit.com/r/AcademicIntegrity/hot.json) instead of the
OAuth API, so no Reddit app credentials are needed. Reddit does block
requests with a generic/missing User-Agent, so set REDDIT_USER_AGENT in
.env to something identifying (Reddit's own guidance:
"<platform>:<app id>:<version> (by /u/<your reddit username>)").

Posts go into the reddit_posts table (see app/models/reddit_post.py),
not the cases table — a scraped post has no real school/workflow/
allegation type to satisfy those required foreign keys.

Run with:
  python fetch_reddit_posts.py
  python fetch_reddit_posts.py --subreddits AcademicIntegrity,college --listing new --limit 50
"""

import argparse
import os
import time
from datetime import datetime, timezone

import requests

from app import create_app
from app.extensions import db
from app.models import RedditPost

DEFAULT_SUBREDDITS = ["AcademicIntegrity", "college", "professors"]
DEFAULT_USER_AGENT = "CaseNext/0.1 (academic integrity research script)"
LISTING_URL = "https://www.reddit.com/r/{subreddit}/{listing}.json"
SECONDS_BETWEEN_SUBREDDITS = 2


def fetch_listing(subreddit, listing, limit, user_agent):
    """Fetch one page of a subreddit's public JSON listing."""
    response = requests.get(
        LISTING_URL.format(subreddit=subreddit, listing=listing),
        headers={"User-Agent": user_agent},
        params={"limit": min(limit, 100)},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def upsert_post(post_data):
    """Insert or update a RedditPost row from one listing child's `data`."""
    post = RedditPost.query.filter_by(post_id=post_data["id"]).first()
    if post is None:
        post = RedditPost(post_id=post_data["id"])
        db.session.add(post)

    post.subreddit = post_data["subreddit"]
    post.title = post_data["title"][:500]
    post.body = post_data.get("selftext") or None
    post.url = f"https://www.reddit.com{post_data['permalink']}"
    post.author = post_data.get("author")
    post.score = post_data.get("score")
    post.num_comments = post_data.get("num_comments")
    post.posted_at = datetime.fromtimestamp(
        post_data["created_utc"], tz=timezone.utc
    ).replace(tzinfo=None)
    post.fetched_at = datetime.utcnow()
    return post


def fetch_subreddit(subreddit, listing, limit, user_agent):
    try:
        data = fetch_listing(subreddit, listing, limit, user_agent)
    except requests.RequestException as err:
        print(f"  ! failed to fetch r/{subreddit}: {err}")
        return 0

    children = data.get("data", {}).get("children", [])
    count = 0
    for child in children:
        if child.get("kind") != "t3":  # t3 = link/text post; skip anything else
            continue
        upsert_post(child["data"])
        count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--subreddits",
        default=",".join(DEFAULT_SUBREDDITS),
        help="Comma-separated subreddit names, no 'r/' prefix",
    )
    parser.add_argument(
        "--listing", default="hot", choices=["hot", "new", "top"], help="Listing to fetch"
    )
    parser.add_argument(
        "--limit", type=int, default=25, help="Posts per subreddit (max 100)"
    )
    args = parser.parse_args()

    user_agent = os.environ.get("REDDIT_USER_AGENT", DEFAULT_USER_AGENT)
    subreddits = [s.strip() for s in args.subreddits.split(",") if s.strip()]

    app = create_app()
    with app.app_context():
        total = 0
        for i, subreddit in enumerate(subreddits):
            print(f"Fetching r/{subreddit} ({args.listing})...")
            count = fetch_subreddit(subreddit, args.listing, args.limit, user_agent)
            db.session.commit()
            print(f"  -> {count} posts upserted")
            total += count
            if i < len(subreddits) - 1:
                time.sleep(SECONDS_BETWEEN_SUBREDDITS)

        print(f"Done. Upserted {total} posts across {len(subreddits)} subreddits.")


if __name__ == "__main__":
    main()
