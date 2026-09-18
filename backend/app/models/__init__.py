"""Import every model here so Flask-Migrate can discover them.

Flask-SQLAlchemy only knows about a table once its model class has been
imported somewhere. Importing them all in this file, and importing this
file from the app factory, guarantees they're registered before we
generate migrations.
"""

from app.models.school import School
from app.models.office import Office
from app.models.terminology import Terminology
from app.models.workflow import Workflow
from app.models.workflow_step import WorkflowStep
from app.models.allegation_type import AllegationType
from app.models.resource import Resource
from app.models.case import Case
from app.models.case_details import CaseDetails
from app.models.case_event import CaseEvent
from app.models.case_outcome import CaseOutcome

__all__ = [
    "School",
    "Office",
    "Terminology",
    "Workflow",
    "WorkflowStep",
    "AllegationType",
    "Resource",
    "Case",
    "CaseDetails",
    "CaseEvent",
    "CaseOutcome",
]
