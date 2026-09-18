from app.extensions import db


class Terminology(db.Model):
    """Stores a school's actual wording for a concept.

    `term` is the school's real term (e.g. "Academic Integrity Meeting").
    `category` is a lightweight, shared label used only for search/filter
    across schools (e.g. "meeting") — it never replaces `term` in the UI.
    """

    __tablename__ = "terminology"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)

    term = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    definition = db.Column(db.Text)

    school = db.relationship("School", back_populates="terminology_entries")

    def __repr__(self):
        return f"<Terminology {self.term}>"
