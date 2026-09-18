from app.extensions import db


class WorkflowStep(db.Model):
    """One stage within a specific school's Workflow.

    This is intentionally school-specific — we never assume two schools
    share the same stages. `order` controls display/sequence order within
    the parent workflow (1, 2, 3, ...). `actor` names who is responsible
    for the step (e.g. "Academic Integrity Officer", "Hearing Panel").
    """

    __tablename__ = "workflow_steps"

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"), nullable=False)

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)
    actor = db.Column(db.String(255))
    entry_conditions = db.Column(db.Text)
    exit_conditions = db.Column(db.Text)

    workflow = db.relationship("Workflow", back_populates="steps")
    cases_currently_here = db.relationship("Case", back_populates="current_step")

    def __repr__(self):
        return f"<WorkflowStep {self.order}: {self.name}>"
