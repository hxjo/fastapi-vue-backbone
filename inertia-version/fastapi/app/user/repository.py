from typing import cast

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.exceptions import InvalidCredentialsException
from app.auth.models import Token
from app.auth.utils.auth import (
    create_access_token,
    get_password_hash,
    verify_password_against_hash,
)
from app.auth.utils.password import is_strong_password
from app.common.deps.common import StructuredCommonDeps
from app.common.exceptions import NotFoundException
from app.common.repository import (
    BaseRepo,
    UpdateSchemaOrDict,
    get_dict_from_obj_in_update,
)
from app.user.fga import UserFGA, UserRole
from app.user.exceptions import (
    EmailAlreadyRegisteredException,
    PasswordNotStrongException,
)
from app.user.models import User, UserCreate, UserUpdate


class UserRepoClass(BaseRepo[User, UserCreate, UserUpdate]):
    async def callback_create(
        self, db_obj: User, *, deps: StructuredCommonDeps
    ) -> None:
        user_id = cast(int, db_obj.id)
        user_role = "client" if not db_obj.is_superuser else "superuser"
        deps.tasks.add_task(
            UserFGA.create_relationships,
            deps.fga_client,
            user_id,
            cast(UserRole, user_role),
            None
        )
        deps.tasks.add_task(deps.search.user.add_documents, [db_obj])

    async def callback_delete(
        self, db_obj: User, *, deps: StructuredCommonDeps
    ) -> None:
        user_id = cast(int, db_obj.id)
        user_role = "superuser" if db_obj.is_superuser else "client"
        deps.tasks.add_task(
            UserFGA.delete_relationships,
            deps.fga_client,
            user_id,
            cast(UserRole, user_role),
        )
        deps.tasks.add_task(deps.search.user.delete_document, db_obj)

    async def callback_update(
        self, db_obj: User, *, deps: StructuredCommonDeps
    ) -> None:
        deps.tasks.add_task(deps.search.user.update_documents, [db_obj])

    async def get_by_email(self, session: AsyncSession, *, email: str) -> User:
        stmt = select(User).where(User.email == email)
        res = await session.exec(stmt)
        user = res.first()
        if user is None:
            raise NotFoundException("user")
        return user

    async def create(
        self,
        deps: StructuredCommonDeps,
        *,
        obj_in: UserCreate,
    ) -> User:
        session = deps.session
        result = is_strong_password(obj_in.password)
        if result is False:
            raise PasswordNotStrongException()
        hashed_password = get_password_hash(obj_in.password)
        obj_in_data = obj_in.model_dump()
        del obj_in_data["password"]
        obj_in_data["hashed_password"] = hashed_password
        db_obj = User(**obj_in_data)
        session.add(db_obj)
        try:
            await session.commit()
        except IntegrityError as exc:
            await session.rollback()
            raise EmailAlreadyRegisteredException() from exc
        await session.refresh(db_obj)
        await self.callback_create(db_obj, deps=deps)
        return db_obj

    async def update(
        self,
        deps: StructuredCommonDeps,
        *,
        id_: int,
        obj_in: UpdateSchemaOrDict[UserUpdate],
    ) -> User:
        update_data = get_dict_from_obj_in_update(obj_in)
        update_password: str | None = update_data.get("password", None)
        if update_password:
            result = is_strong_password(update_password)
            if result is False:
                raise PasswordNotStrongException()
            hashed_password = get_password_hash(update_password)
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        try:
            return await super().update(deps, id_=id_, obj_in=update_data)
        except IntegrityError as exc:
            raise EmailAlreadyRegisteredException() from exc

    async def authenticate(
        self, session: AsyncSession, *, email: str, password: str
    ) -> Token:
        try:
            db_user = await self.get_by_email(session, email=email)
        except NotFoundException as exc:
            raise InvalidCredentialsException() from exc
        if not verify_password_against_hash(password, db_user.hashed_password):
            raise InvalidCredentialsException()

        access_token = create_access_token(
            data={"email": db_user.email},
        )
        return Token(access_token=access_token)

    async def set_avatar_url(
        self, session: AsyncSession, id_: int, avatar: UploadFile
    ) -> User:
        user = await self.get(session, id_=id_)
        user.avatar_url = avatar
        await session.commit()
        await session.refresh(user)
        return user


UserRepo = UserRepoClass(model=User)
