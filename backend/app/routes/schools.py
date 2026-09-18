from flask import Blueprint, jsonify

from app.extensions import db
from app.models import (
    School,
    Office,
    Terminology,
    Workflow,
    AllegationType,
    Resource,
)

schools_bp = Blueprint("schools", __name__, url_prefix="/api/schools")


@schools_bp.route("", methods=["GET"])
def list_schools():
    schools = School.query.order_by(School.name).all()
    return jsonify([school.to_dict() for school in schools])


@schools_bp.route("/<int:school_id>", methods=["GET"])
def get_school(school_id):
    school = db.get_or_404(School, school_id)
    return jsonify(school.to_dict())


@schools_bp.route("/<int:school_id>/offices", methods=["GET"])
def list_offices(school_id):
    db.get_or_404(School, school_id)
    offices = Office.query.filter_by(school_id=school_id).order_by(Office.name).all()
    return jsonify([office.to_dict() for office in offices])


@schools_bp.route("/<int:school_id>/terminology", methods=["GET"])
def list_terminology(school_id):
    db.get_or_404(School, school_id)
    entries = (
        Terminology.query.filter_by(school_id=school_id)
        .order_by(Terminology.term)
        .all()
    )
    return jsonify([entry.to_dict() for entry in entries])


@schools_bp.route("/<int:school_id>/workflows", methods=["GET"])
def list_workflows(school_id):
    db.get_or_404(School, school_id)
    workflows = Workflow.query.filter_by(school_id=school_id).order_by(Workflow.name).all()
    return jsonify([workflow.to_dict(include_steps=True) for workflow in workflows])


@schools_bp.route("/<int:school_id>/allegation-types", methods=["GET"])
def list_allegation_types(school_id):
    db.get_or_404(School, school_id)
    allegation_types = (
        AllegationType.query.filter_by(school_id=school_id)
        .order_by(AllegationType.name)
        .all()
    )
    return jsonify([allegation_type.to_dict() for allegation_type in allegation_types])


@schools_bp.route("/<int:school_id>/resources", methods=["GET"])
def list_resources(school_id):
    db.get_or_404(School, school_id)
    resources = (
        Resource.query.filter_by(school_id=school_id).order_by(Resource.title).all()
    )
    return jsonify([resource.to_dict() for resource in resources])
