from app.extensions import db


class RedditPost(db.Model):
    """A post scraped from a subreddit's public JSON listing.

    Kept separate from Case on purpose: Case rows require a real school,
    workflow, and allegation type (all NOT NULL foreign keys), which a
    scraped Reddit post doesn't have. This table just stores what was
    scraped so it can be browsed/mined on its own.
    """

    __tablename__ = "reddit_posts"

    id = db.Column(db.Integer, primary_key=True)

    # Reddit's own post id (the part after "t3_"), e.g. "1abcde".
    # Unique so re-fetching a listing doesn't create duplicate rows.
    post_id = db.Column(db.String(20), nullable=False, unique=True)

    subreddit = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text)
    url = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(100))
    score = db.Column(db.Integer)
    num_comments = db.Column(db.Integer)

    posted_at = db.Column(db.DateTime, nullable=False)
    fetched_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<RedditPost r/{self.subreddit} {self.post_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "subreddit": self.subreddit,
            "title": self.title,
            "body": self.body,
            "url": self.url,
            "author": self.author,
            "score": self.score,
            "num_comments": self.num_comments,
            "posted_at": self.posted_at.isoformat() if self.posted_at else None,
            "fetched_at": self.fetched_at.isoformat() if self.fetched_at else None,
        }
