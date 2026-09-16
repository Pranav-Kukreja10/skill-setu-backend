from ninja import NinjaAPI
from ninja.errors import ValidationError
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import OperationalError, IntegrityError, DatabaseError
from django.http import Http404
import logging

from accounts.api import router as accounts_router
from students.api import router as students_router, schemes_router
from recruiters.api import (
    recruiters_router,
    listings_router,
    applications_router,
    programs_router
)
from institutions.api import (
    placement_router,
    institutions_router
)

logger = logging.getLogger("skillsetu.api")

api = NinjaAPI(
    title="Skill Setu API",
    version="1.0.0",
    docs_url="/docs"
)

@api.exception_handler(ValidationError)
def validation_error_handler(request, exc: ValidationError):
    return api.create_response(
        request,
        {
            "status": "error",
            "code": "VALIDATION_ERROR",
            "message": "Validation failed for incoming request parameters.",
            "details": exc.errors
        },
        status=422
    )

@api.exception_handler(ObjectDoesNotExist)
@api.exception_handler(Http404)
def not_found_handler(request, exc):
    return api.create_response(
        request,
        {
            "status": "error",
            "code": "NOT_FOUND",
            "message": str(exc) if str(exc) else "Requested resource was not found."
        },
        status=404
    )

@api.exception_handler(PermissionDenied)
def permission_denied_handler(request, exc: PermissionDenied):
    return api.create_response(
        request,
        {
            "status": "error",
            "code": "FORBIDDEN",
            "message": str(exc) if str(exc) else "You do not have permission to perform this action."
        },
        status=403
    )

@api.exception_handler(OperationalError)
def operational_error_handler(request, exc: OperationalError):
    logger.warning(f"Database row contention or operational error: {exc}")
    return api.create_response(
        request,
        {
            "status": "error",
            "code": "CONCURRENCY_CONFLICT",
            "message": "Database row contention: Operation locked by a concurrent transaction. Please retry."
        },
        status=409
    )

@api.exception_handler(IntegrityError)
def integrity_error_handler(request, exc: IntegrityError):
    logger.error(f"Database integrity violation: {exc}")
    return api.create_response(
        request,
        {
            "status": "error",
            "code": "INTEGRITY_ERROR",
            "message": "A database constraint violation occurred (e.g. duplicate key or foreign key dependency)."
        },
        status=400
    )

@api.exception_handler(DatabaseError)
def database_error_handler(request, exc: DatabaseError):
    logger.error(f"Database system error: {exc}")
    return api.create_response(
        request,
        {
            "status": "error",
            "code": "DATABASE_ERROR",
            "message": "A transient database error occurred. The operation has been safely aborted."
        },
        status=503
    )

@api.exception_handler(Exception)
def global_internal_error_handler(request, exc: Exception):
    logger.exception(f"Unhandled internal server error: {exc}")
    return api.create_response(
        request,
        {
            "status": "error",
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected server error occurred. Our engineers have been alerted."
        },
        status=500
    )

api.add_router("/auth", accounts_router)
api.add_router("/students", students_router)
api.add_router("/schemes", schemes_router)
api.add_router("/recruiters", recruiters_router)
api.add_router("/listings", listings_router)
api.add_router("/applications", applications_router)
api.add_router("/programs", programs_router)
api.add_router("/placement", placement_router)
api.add_router("/institutions", institutions_router)
