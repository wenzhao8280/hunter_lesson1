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

    def to_dict(self, include_relations=False, include_summary=False):
        data = {
            "id": self.id,
            "school_id": self.school_id,
            "workflow_id": self.workflow_id,
            "current_step_id": self.current_step_id,
            "allegation_type_id": self.allegation_type_id,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_summary:
            # Names only, for list views (e.g. Case Database) that don't
            # need the full nested workflow/events/outcomes payload.
            data["school_name"] = self.school.name if self.school else None
            data["workflow_name"] = self.workflow.name if self.workflow else None
            data["current_step_name"] = (
                self.current_step.name if self.current_step else None
            )
            data["allegation_type_name"] = (
                self.allegation_type.name if self.allegation_type else None
            )
        if include_relations:
            data["school"] = self.school.to_dict() if self.school else None
            data["workflow"] = (
                self.workflow.to_dict(include_steps=True) if self.workflow else None
            )
            data["current_step"] = (
                self.current_step.to_dict() if self.current_step else None
            )
            data["allegation_type"] = (
                self.allegation_type.to_dict() if self.allegation_type else None
            )
            data["details"] = self.details.to_dict() if self.details else None
            data["events"] = [event.to_dict() for event in self.events]
            data["outcomes"] = [outcome.to_dict() for outcome in self.outcomes]
        return data
