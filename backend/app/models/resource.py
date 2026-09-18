from app.extensions import db


class Resource(db.Model):
    """An official link/document a school publishes (policy, forms, etc.)."""

    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)

    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    last_verified_at = db.Column(db.DateTime)

    school = db.relationship("School", back_populates="resources")

    def __repr__(self):
        return f"<Resource {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "school_id": self.school_id,
            "title": self.title,
            "category": self.category,
            "url": self.url,
            "description": self.description,
            "last_verified_at": (
                self.last_verified_at.isoformat() if self.last_verified_at else None
            ),
        }
