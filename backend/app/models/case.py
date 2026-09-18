from datetime import datetime

from app.extensions import db


class Case(db.Model):
    """One student's academic misconduct case.

    This row describes what the case CURRENTLY is (which school, which
    workflow, which step it's at, what it's alleged to be, and its
    status). What has HAPPENED over time lives in CaseEvent, not here.
    """

    __tablename__ = "cases"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"), nullable=False)
    current_step_id = db.Column(
        db.Integer, db.ForeignKey("workflow_steps.id"), nullable=True
    )
    allegation_type_id = db.Column(
        db.Integer, db.ForeignKey("allegation_types.id"), nullable=False
    )

    # active | resolved | appealed
    status = db.Column(db.String(50), nullable=False, default="active")

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    school = db.relationship("School", back_populates="cases")
    workflow = db.relationship("Workflow", back_populates="cases")
    current_step = db.relationship("WorkflowStep", back_populates="cases_currently_here")
    allegation_type = db.relationship("AllegationType", back_populates="cases")

    details = db.relationship(
        "CaseDetails",
        back_populates="case",
        uselist=False,  # one-to-one: a Case has exactly one CaseDetails
        cascade="all, delete-orphan",
    )
    events = db.relationship(
        "CaseEvent",
        back_populates="case",
        cascade="all, delete-orphan",
        order_by="CaseEvent.event_date",
    )
    outcomes = db.relationship(
        "CaseOutcome", back_populates="case", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Case {self.id} status={self.status}>"
