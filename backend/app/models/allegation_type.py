from app.extensions import db


class AllegationType(db.Model):
    """A type of misconduct allegation as a specific school names it.

    `name` preserves the school's actual wording (e.g. "Unauthorized
    Collaboration"). `category` is only a lightweight, shared label for
    cross-school search/filtering (e.g. "collaboration") and is never
    shown as a replacement for the school's own term.
    """

    __tablename__ = "allegation_types"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))

    school = db.relationship("School", back_populates="allegation_types")
    cases = db.relationship("Case", back_populates="allegation_type")

    def __repr__(self):
        return f"<AllegationType {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "school_id": self.school_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
        }
