from datetime import date, datetime

from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import (
    School,
    Workflow,
    WorkflowStep,
    AllegationType,
    Case,
    CaseDetails,
    CaseEvent,
    CaseOutcome,
)

cases_bp = Blueprint("cases", __name__, url_prefix="/api/cases")

VALID_CASE_STATUSES = {"active", "resolved", "appealed"}
VALID_EVENT_SOURCES = {"student", "official"}


def _error(message, status=400):
    return jsonify({"error": message}), status


def _parse_date(value):
    """Parse an 'YYYY-MM-DD' string into a date, or raise ValueError."""
    return date.fromisoformat(value)


def _parse_datetime(value):
    """Parse an ISO 8601 string into a datetime, or raise ValueError."""
    return datetime.fromisoformat(value)


@cases_bp.route("", methods=["GET"])
def list_cases():
    query = Case.query
    school_id = request.args.get("school_id", type=int)
    if school_id is not None:
        query = query.filter_by(school_id=school_id)
    status = request.args.get("status")
    if status is not None:
        query = query.filter_by(status=status)
    cases = query.order_by(Case.created_at.desc()).all()
    return jsonify([case.to_dict(include_summary=True) for case in cases])


@cases_bp.route("", methods=["POST"])
def create_case():
    payload = request.get_json(silent=True) or {}

    for field in ("school_id", "workflow_id", "allegation_type_id"):
        if not payload.get(field):
            return _error(f"'{field}' is required")

    school = db.session.get(School, payload["school_id"])
    if school is None:
        return _error(f"No school with id {payload['school_id']}", 404)

    workflow = db.session.get(Workflow, payload["workflow_id"])
    if workflow is None or workflow.school_id != school.id:
        return _error("workflow_id must belong to the given school")

    allegation_type = db.session.get(AllegationType, payload["allegation_type_id"])
    if allegation_type is None or allegation_type.school_id != school.id:
        return _error("allegation_type_id must belong to the given school")

    current_step_id = payload.get("current_step_id")
    if current_step_id is not None:
        step = db.session.get(WorkflowStep, current_step_id)
        if step is None or step.workflow_id != workflow.id:
            return _error("current_step_id must belong to the given workflow")

    status = payload.get("status", "active")
    if status not in VALID_CASE_STATUSES:
        return _error(f"status must be one of {sorted(VALID_CASE_STATUSES)}")

    case = Case(
        school_id=school.id,
        workflow_id=workflow.id,
        allegation_type_id=allegation_type.id,
        current_step_id=current_step_id,
        status=status,
    )
    db.session.add(case)
    db.session.commit()
    return jsonify(case.to_dict(include_relations=True)), 201


@cases_bp.route("/<int:case_id>", methods=["GET"])
def get_case(case_id):
    case = db.get_or_404(Case, case_id)
    return jsonify(case.to_dict(include_relations=True))


@cases_bp.route("/<int:case_id>", methods=["PATCH"])
def update_case(case_id):
    case = db.get_or_404(Case, case_id)
    payload = request.get_json(silent=True) or {}

    if "status" in payload:
        if payload["status"] not in VALID_CASE_STATUSES:
            return _error(f"status must be one of {sorted(VALID_CASE_STATUSES)}")
        case.status = payload["status"]

    if "current_step_id" in payload:
        current_step_id = payload["current_step_id"]
        if current_step_id is not None:
            step = db.session.get(WorkflowStep, current_step_id)
            if step is None or step.workflow_id != case.workflow_id:
                return _error("current_step_id must belong to the case's workflow")
        case.current_step_id = current_step_id

    db.session.commit()
    return jsonify(case.to_dict(include_relations=True))


@cases_bp.route("/<int:case_id>/details", methods=["PUT"])
def upsert_case_details(case_id):
    case = db.get_or_404(Case, case_id)
    payload = request.get_json(silent=True) or {}

    details = case.details or CaseDetails(case_id=case.id)

    for field in (
        "course_name",
        "course_code",
        "student_description",
        "has_evidence",
        "notes",
    ):
        if field in payload:
            setattr(details, field, payload[field])

    for date_field in ("incident_date", "notice_date"):
        if date_field in payload:
            value = payload[date_field]
            if not value:
                setattr(details, date_field, None)
                continue
            try:
                setattr(details, date_field, _parse_date(value))
            except ValueError:
                return _error(f"'{date_field}' must be an ISO date (YYYY-MM-DD)")

    db.session.add(details)
    db.session.commit()
    return jsonify(details.to_dict())


@cases_bp.route("/<int:case_id>/events", methods=["GET"])
def list_case_events(case_id):
    db.get_or_404(Case, case_id)
    events = (
        CaseEvent.query.filter_by(case_id=case_id).order_by(CaseEvent.event_date).all()
    )
    return jsonify([event.to_dict() for event in events])


@cases_bp.route("/<int:case_id>/events", methods=["POST"])
def create_case_event(case_id):
    case = db.get_or_404(Case, case_id)
    payload = request.get_json(silent=True) or {}

    for field in ("title", "event_date"):
        if not payload.get(field):
            return _error(f"'{field}' is required")

    source = payload.get("source", "student")
    if source not in VALID_EVENT_SOURCES:
        return _error(f"source must be one of {sorted(VALID_EVENT_SOURCES)}")

    try:
        event_date = _parse_datetime(payload["event_date"])
    except ValueError:
        return _error("'event_date' must be an ISO 8601 datetime")

    event = CaseEvent(
        case_id=case.id,
        event_type=payload.get("event_type"),
        title=payload["title"],
        description=payload.get("description"),
        event_date=event_date,
        source=source,
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201


@cases_bp.route("/<int:case_id>/outcomes", methods=["GET"])
def list_case_outcomes(case_id):
    db.get_or_404(Case, case_id)
    outcomes = CaseOutcome.query.filter_by(case_id=case_id).all()
    return jsonify([outcome.to_dict() for outcome in outcomes])


@cases_bp.route("/<int:case_id>/outcomes", methods=["POST"])
def create_case_outcome(case_id):
    case = db.get_or_404(Case, case_id)
    payload = request.get_json(silent=True) or {}

    if not payload.get("outcome_type"):
        return _error("'outcome_type' is required")

    outcome_date = None
    if payload.get("date"):
        try:
            outcome_date = _parse_date(payload["date"])
        except ValueError:
            return _error("'date' must be an ISO date (YYYY-MM-DD)")

    outcome = CaseOutcome(
        case_id=case.id,
        outcome_type=payload["outcome_type"],
        description=payload.get("description"),
        official=payload.get("official", False),
        date=outcome_date,
    )
    db.session.add(outcome)
    db.session.commit()
    return jsonify(outcome.to_dict()), 201
