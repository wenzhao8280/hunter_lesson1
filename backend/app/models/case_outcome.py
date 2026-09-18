from app.extensions import db


class CaseOutcome(db.Model):
    """A recorded result of a case (e.g. "Warning", "No violation found").

    `official` distinguishes a result the school issued from one the
    student self-reported. There is intentionally no "guilty" field —
    CaseNext does not judge or determine misconduct.
    """

    __tablename__ = "case_outcomes"

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey("cases.id"), nullable=False)

    outcome_type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    official = db.Column(db.Boolean, default=False, nullable=False)
    date = db.Column(db.Date)

    case = db.relationship("Case", back_populates="outcomes")

    def __repr__(self):
        return f"<CaseOutcome {self.outcome_type}>"
