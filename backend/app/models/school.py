from app.extensions import db


class School(db.Model):
    """A university using CaseNext.

    Every other school-specific table (offices, terminology, workflows,
    allegation types, resources, cases) hangs off this one, so we never
    mix up which rules/terms belong to which school.
    """

    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(255), unique=True, nullable=False)
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))

    # Relationships back to this school. `cascade="all, delete-orphan"`
    # means: if a School row is deleted, its child rows go with it
    # (useful in a small MVP; we can revisit for production).
    offices = db.relationship(
        "Office", back_populates="school", cascade="all, delete-orphan"
    )
    terminology_entries = db.relationship(
        "Terminology", back_populates="school", cascade="all, delete-orphan"
    )
    workflows = db.relationship(
        "Workflow", back_populates="school", cascade="all, delete-orphan"
    )
    allegation_types = db.relationship(
        "AllegationType", back_populates="school", cascade="all, delete-orphan"
    )
    resources = db.relationship(
        "Resource", back_populates="school", cascade="all, delete-orphan"
    )
    cases = db.relationship(
        "Case", back_populates="school", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<School {self.name}>"
