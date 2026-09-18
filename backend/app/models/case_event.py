from datetime import datetime

from app.extensions import db


class CaseEvent(db.Model):
    """Something that happened during a case — the timeline entries.

    Do not confuse with Case: Case is the current state, CaseEvent is
    the history (e.g. "Sep 1 - notice received", "Sep 8 - meeting
    scheduled"). `source` records whether the student or the school
    logged it ("student" or "official").
    """

    __tablename__ = "case_events"

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey("cases.id"), nullable=False)

    event_type = db.Column(db.String(100))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)

    # student | official
    source = db.Column(db.String(50), nullable=False, default="student")

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    case = db.relationship("Case", back_populates="events")

    def __repr__(self):
        return f"<CaseEvent {self.title} on {self.event_date}>"

    def to_dict(self):
        return {
            "id": self.id,
            "case_id": self.case_id,
            "event_type": self.event_type,
            "title": self.title,
            "description": self.description,
            "event_date": self.event_date.isoformat() if self.event_date else None,
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
