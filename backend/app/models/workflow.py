from app.extensions import db


class Workflow(db.Model):
    """A named process a school follows for misconduct cases.

    A school could in theory have more than one workflow (e.g. one for
    undergraduate cases, one for graduate cases), which is why this is
    its own table rather than a fixed set of steps on School directly.
    """

    __tablename__ = "workflows"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    school = db.relationship("School", back_populates="workflows")
    steps = db.relationship(
        "WorkflowStep",
        back_populates="workflow",
        cascade="all, delete-orphan",
        order_by="WorkflowStep.order",
    )
    cases = db.relationship("Case", back_populates="workflow")

    def __repr__(self):
        return f"<Workflow {self.name}>"

    def to_dict(self, include_steps=False):
        data = {
            "id": self.id,
            "school_id": self.school_id,
            "name": self.name,
            "description": self.description,
        }
        if include_steps:
            data["steps"] = [step.to_dict() for step in self.steps]
        return data
