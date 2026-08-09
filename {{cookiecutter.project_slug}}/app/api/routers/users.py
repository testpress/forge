"""User management endpoints.

These are async and talk to Django's async ORM directly (``afirst``,
``acount``, ``async for``, ``adelete``) - no thread pool, no second data
access layer, and the same models the admin and the rest of the site use.
"""

from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import paginate

from app.api.schemas.users import UserCreateSchema
from app.api.schemas.users import UserSchema
from app.api.schemas.users import UserUpdateSchema
from app.models import User

router = Router()

USER_NOT_FOUND = "User not found"
PHONE_NUMBER_TAKEN = "That phone number is already registered"


async def _get_user_or_404(user_id: int) -> User:
    user = await User.objects.filter(pk=user_id).afirst()
    if user is None:
        raise HttpError(404, USER_NOT_FOUND)
    return user


@router.get("/", response=list[UserSchema])
@paginate
async def list_users(request: HttpRequest):
    """List users, newest last.

    ``@paginate`` wraps the response in ``{"items": [...], "count": n}`` and
    reads ``?limit=`` / ``?offset=`` from the query string.
    """
    return User.objects.order_by("id")


@router.get("/{int:user_id}", response=UserSchema)
async def get_user(request: HttpRequest, user_id: int) -> User:
    """Fetch a single user."""
    return await _get_user_or_404(user_id)


@router.post("/", response={201: UserSchema})
async def create_user(request: HttpRequest, payload: UserCreateSchema) -> tuple:
    """Create a user.

    Goes through ``UserManager.acreate_user`` so the password is hashed by
    Django and the accompanying ``Profile`` row is created, exactly as it
    would be from ``manage.py createsuperuser``.

    The duplicate check is a query rather than a caught ``IntegrityError``
    because letting the constraint fire would poison the surrounding
    transaction and turn a 409 into a 500 on the next query.
    """
    taken = await User.objects.filter(phone_number=payload.phone_number).aexists()
    if taken:
        raise HttpError(409, PHONE_NUMBER_TAKEN)

    user = await User.objects.acreate_user(
        phone_number=payload.phone_number,
        password=payload.password,
        email=payload.email,
    )
    return 201, user


@router.patch("/{int:user_id}", response=UserSchema)
async def update_user(
    request: HttpRequest,
    user_id: int,
    payload: UserUpdateSchema,
) -> User:
    """Apply a partial update."""
    user = await _get_user_or_404(user_id)

    changed = payload.model_dump(exclude_unset=True, exclude_none=True)
    for field, value in changed.items():
        setattr(user, field, value)

    if changed:
        await user.asave(update_fields=list(changed))

    return user


@router.delete("/{int:user_id}", response={204: None})
async def delete_user(request: HttpRequest, user_id: int) -> tuple:
    """Soft-delete a user.

    Deleted through the queryset rather than the instance: Django's
    `Model.adelete()` forwards `keep_parents` down to `save()`, which
    django-safedelete's soft-delete path does not accept, so
    `user.adelete()` raises TypeError on any SafeDeleteModel.
    """
    await _get_user_or_404(user_id)
    await User.objects.filter(pk=user_id).adelete()
    return 204, None
