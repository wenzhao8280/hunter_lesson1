from app.extensions import db


class Office(db.Model):
    """A school department/office involved in misconduct cases.

    Example: "Office of Academic Integrity", "Dean of Students".
    Kept separate from Terminology because an office is an actual entity
    with contact info, not just a word.
    """

    __tablename__ = "offices"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)

    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100))
    description = db.Column(db.Text)
    website = db.Column(db.String(500))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(50))

    school = db.relationship("School", back_populates="offices")

    def __repr__(self):
        return f"<Office {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "school_id": self.school_id,
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "website": self.website,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
        }
