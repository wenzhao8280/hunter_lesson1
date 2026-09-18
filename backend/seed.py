"""Populate the database with sample schools for local development/demo.

Run with:  python seed.py
This wipes and re-creates all rows in the tables below, so only run it
against a dev database.

Two schools are seeded on purpose, with deliberately different
terminology and workflow steps, to prove the schema doesn't force a
one-size-fits-all process onto every school.
"""

from datetime import date, datetime

from app import create_app
from app.extensions import db
from app.models import (
    AllegationType,
    Case,
    CaseDetails,
    CaseEvent,
    CaseOutcome,
    Office,
    Resource,
    School,
    Terminology,
    Workflow,
    WorkflowStep,
)


def clear_data():
    # Delete in an order that respects foreign keys.
    CaseOutcome.query.delete()
    CaseEvent.query.delete()
    CaseDetails.query.delete()
    Case.query.delete()
    WorkflowStep.query.delete()
    Workflow.query.delete()
    AllegationType.query.delete()
    Resource.query.delete()
    Terminology.query.delete()
    Office.query.delete()
    School.query.delete()
    db.session.commit()


def seed_asu():
    """Arizona State University — uses "Academic Integrity" terminology."""
    school = School(
        name="Arizona State University",
        domain="asu.edu",
        state="Arizona",
        country="USA",
    )
    db.session.add(school)
    db.session.flush()  # get school.id without a full commit

    db.session.add(
        Office(
            school_id=school.id,
            name="Office of Academic Integrity",
            type="academic_integrity_office",
            description="Handles undergraduate and graduate academic integrity cases.",
            website="https://provost.asu.edu/academic-integrity",
            contact_email="academicintegrity@asu.edu",
            contact_phone="480-555-0100",
        )
    )

    for term, category, definition in [
        ("Academic Integrity Officer", "official_role", "The staff member who reviews and manages a case."),
        ("Academic Integrity Meeting", "meeting", "A meeting between the student and the Academic Integrity Officer to discuss the allegation."),
        ("Appeal", "appeal", "A formal request to review the outcome of a case."),
    ]:
        db.session.add(Terminology(school_id=school.id, term=term, category=category, definition=definition))

    workflow = Workflow(
        school_id=school.id,
        name="ASU Academic Integrity Process",
        description="Standard process for handling academic integrity allegations at ASU.",
    )
    db.session.add(workflow)
    db.session.flush()

    steps_data = [
        ("Notice Issued", "The Academic Integrity Officer notifies the student of the allegation.", 1, "Academic Integrity Officer", "Faculty member reports suspected violation.", "Student acknowledges receipt of notice."),
        ("Student Response", "The student submits a written response to the allegation.", 2, "Student", "Notice has been issued.", "Response submitted or response window expires."),
        ("Academic Integrity Meeting", "The student meets with the Academic Integrity Officer to discuss the case.", 3, "Academic Integrity Officer", "Student response received or window expired.", "Meeting is completed."),
        ("Decision Issued", "The Academic Integrity Officer issues a decision and any sanctions.", 4, "Academic Integrity Officer", "Meeting completed.", "Decision letter sent to student."),
        ("Appeal (optional)", "The student may appeal the decision to the Academic Integrity Appeals Board.", 5, "Academic Integrity Appeals Board", "Student files an appeal within the deadline.", "Appeal board issues final decision."),
    ]
    steps = []
    for name, description, order, actor, entry, exit_ in steps_data:
        step = WorkflowStep(
            workflow_id=workflow.id,
            name=name,
            description=description,
            order=order,
            actor=actor,
            entry_conditions=entry,
            exit_conditions=exit_,
        )
        db.session.add(step)
        steps.append(step)
    db.session.flush()

    allegation = AllegationType(
        school_id=school.id,
        name="Plagiarism",
        description="Presenting someone else's work or ideas as your own without proper attribution.",
        category="plagiarism",
    )
    db.session.add(allegation)
    db.session.flush()

    db.session.add_all(
        [
            Resource(
                school_id=school.id,
                title="ASU Academic Integrity Policy",
                category="policy",
                url="https://provost.asu.edu/academic-integrity/policy",
                description="The official university policy defining academic integrity violations and sanctions.",
                last_verified_at=datetime(2025, 8, 1),
            ),
            Resource(
                school_id=school.id,
                title="Academic Integrity Appeal Procedure",
                category="appeal_procedure",
                url="https://provost.asu.edu/academic-integrity/appeals",
                description="Steps and deadlines for filing an appeal.",
                last_verified_at=datetime(2025, 8, 1),
            ),
        ]
    )

    # Sample case at ASU, currently at the "Academic Integrity Meeting" step.
    case = Case(
        school_id=school.id,
        workflow_id=workflow.id,
        current_step_id=steps[2].id,  # Academic Integrity Meeting
        allegation_type_id=allegation.id,
        status="active",
    )
    db.session.add(case)
    db.session.flush()

    db.session.add(
        CaseDetails(
            case_id=case.id,
            course_name="Introduction to Psychology",
            course_code="PSY101",
            incident_date=date(2025, 9, 1),
            notice_date=date(2025, 9, 3),
            student_description="I used a couple of sentences from a website in my essay without citing it properly. I didn't realize it counted as plagiarism.",
            has_evidence=True,
            notes="Student has syllabus and draft history saved.",
        )
    )

    db.session.add_all(
        [
            CaseEvent(
                case_id=case.id,
                event_type="notice",
                title="Academic integrity notice received",
                description="Received an email from the Academic Integrity Officer about a plagiarism allegation in PSY101.",
                event_date=datetime(2025, 9, 3),
                source="official",
            ),
            CaseEvent(
                case_id=case.id,
                event_type="response",
                title="Student response submitted",
                description="Submitted a written explanation and supporting draft history.",
                event_date=datetime(2025, 9, 8),
                source="student",
            ),
            CaseEvent(
                case_id=case.id,
                event_type="meeting_scheduled",
                title="Academic Integrity Meeting scheduled",
                description="Meeting scheduled with the Academic Integrity Officer for Sept 22.",
                event_date=datetime(2025, 9, 12),
                source="official",
            ),
        ]
    )

    return school


def seed_uiuc():
    """University of Illinois Urbana-Champaign — different terminology on purpose."""
    school = School(
        name="University of Illinois Urbana-Champaign",
        domain="illinois.edu",
        state="Illinois",
        country="USA",
    )
    db.session.add(school)
    db.session.flush()

    db.session.add(
        Office(
            school_id=school.id,
            name="Office for Student Conflict Resolution",
            type="student_conduct_office",
            description="Administers the student code and academic integrity proceedings.",
            website="https://conflictresolution.illinois.edu",
            contact_email="osccr@illinois.edu",
            contact_phone="217-555-0199",
        )
    )

    for term, category, definition in [
        ("Preliminary Determination", "official_role", "The instructor's initial written finding of an academic integrity infraction."),
        ("Disciplinary Conference", "meeting", "A conference between the student and a college disciplinary officer to review the case."),
        ("Petition for Review", "appeal", "The formal process for contesting a disciplinary decision."),
    ]:
        db.session.add(Terminology(school_id=school.id, term=term, category=category, definition=definition))

    workflow = Workflow(
        school_id=school.id,
        name="UIUC Student Code Academic Integrity Procedure",
        description="Process defined under the UIUC Student Code for academic integrity infractions.",
    )
    db.session.add(workflow)
    db.session.flush()

    steps_data = [
        ("Instructor Preliminary Determination", "The instructor documents the alleged infraction and notifies the student.", 1, "Instructor", "Instructor suspects an academic integrity infraction.", "Written determination delivered to student and college."),
        ("Student Statement", "The student may submit a statement responding to the determination.", 2, "Student", "Preliminary determination delivered.", "Statement submitted or deadline passes."),
        ("Disciplinary Conference", "A college disciplinary officer meets with the student to review the case.", 3, "Disciplinary Officer", "Student statement period has closed.", "Conference concludes."),
        ("Disciplinary Sanction Letter", "The disciplinary officer issues a sanction letter.", 4, "Disciplinary Officer", "Conference concluded.", "Letter sent to student."),
        ("Petition for Review", "The student may petition the Senate Committee on Student Discipline for review.", 5, "Senate Committee on Student Discipline", "Student files a petition within the deadline.", "Committee issues final ruling."),
    ]
    steps = []
    for name, description, order, actor, entry, exit_ in steps_data:
        step = WorkflowStep(
            workflow_id=workflow.id,
            name=name,
            description=description,
            order=order,
            actor=actor,
            entry_conditions=entry,
            exit_conditions=exit_,
        )
        db.session.add(step)
        steps.append(step)
    db.session.flush()

    allegation = AllegationType(
        school_id=school.id,
        name="Unauthorized Collaboration",
        description="Working with another student on an assignment intended to be completed individually.",
        category="collaboration",
    )
    db.session.add(allegation)
    db.session.flush()

    db.session.add_all(
        [
            Resource(
                school_id=school.id,
                title="UIUC Student Code, Article 1-402",
                category="policy",
                url="https://studentcode.illinois.edu/article1/part4/1-402/",
                description="Official definitions of academic integrity infractions.",
                last_verified_at=datetime(2025, 8, 1),
            ),
            Resource(
                school_id=school.id,
                title="Petition for Review Process",
                category="appeal_procedure",
                url="https://conflictresolution.illinois.edu/petition-for-review",
                description="How to file a petition for review of a disciplinary decision.",
                last_verified_at=datetime(2025, 8, 1),
            ),
        ]
    )

    # Sample resolved case at UIUC, already past the workflow.
    case = Case(
        school_id=school.id,
        workflow_id=workflow.id,
        current_step_id=steps[3].id,  # Disciplinary Sanction Letter
        allegation_type_id=allegation.id,
        status="resolved",
    )
    db.session.add(case)
    db.session.flush()

    db.session.add(
        CaseDetails(
            case_id=case.id,
            course_name="Data Structures",
            course_code="CS225",
            incident_date=date(2025, 2, 10),
            notice_date=date(2025, 2, 20),
            student_description="Shared my code with a classmate on a solo lab assignment.",
            has_evidence=False,
            notes=None,
        )
    )

    db.session.add_all(
        [
            CaseEvent(
                case_id=case.id,
                event_type="notice",
                title="Preliminary determination received",
                description="Instructor sent a preliminary determination for unauthorized collaboration on Lab 4.",
                event_date=datetime(2025, 2, 20),
                source="official",
            ),
            CaseEvent(
                case_id=case.id,
                event_type="response",
                title="Student statement submitted",
                description="Submitted a statement acknowledging the collaboration and explaining the circumstances.",
                event_date=datetime(2025, 2, 24),
                source="student",
            ),
            CaseEvent(
                case_id=case.id,
                event_type="meeting_completed",
                title="Disciplinary Conference completed",
                description="Met with the college disciplinary officer to discuss the case.",
                event_date=datetime(2025, 3, 5),
                source="official",
            ),
            CaseEvent(
                case_id=case.id,
                event_type="decision",
                title="Sanction letter issued",
                description="Received a sanction letter with a grade penalty on the assignment.",
                event_date=datetime(2025, 3, 12),
                source="official",
            ),
        ]
    )

    db.session.add(
        CaseOutcome(
            case_id=case.id,
            outcome_type="Academic Penalty",
            description="Zero grade on Lab 4 and a warning placed on file for one year.",
            official=True,
            date=date(2025, 3, 12),
        )
    )

    return school


def main():
    app = create_app()
    with app.app_context():
        clear_data()
        asu = seed_asu()
        uiuc = seed_uiuc()
        db.session.commit()
        print(f"Seeded schools: {asu.name}, {uiuc.name}")


if __name__ == "__main__":
    main()
