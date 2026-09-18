from app.extensions import db


class CaseDetails(db.Model):
    """Extra descriptive info about a Case, split out to keep Case lean.

    One-to-one with Case (via the unique case_id).
    """

    __tablename__ = "case_details"

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(
        db.Integer, db.ForeignKey("cases.id"), nullable=False, unique=True
    )

    course_name = db.Column(db.String(255))
    course_code = db.Column(db.String(50))
    incident_date = db.Column(db.Date)
    notice_date = db.Column(db.Date)
    student_description = db.Column(db.Text)
    has_evidence = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)

    case = db.relationship("Case", back_populates="details")

    def __repr__(self):
        return f"<CaseDetails for case {self.case_id}>"
