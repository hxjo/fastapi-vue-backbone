from typing import Any, Dict, Generic, Type, TypeAlias, TypeVar, Union, cast

from pydantic import BaseModel
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.deps.common import StructuredCommonDeps
from app.common.exceptions import NotFoundException

ModelT = TypeVar("ModelT", bound=Any)
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)

UpdateSchemaOrDict: TypeAlias = Union[UpdateSchemaT, Dict[str, Any]]


def get_dict_from_obj_in_update(
    obj_in: UpdateSchemaOrDict[UpdateSchemaT],
) -> dict[str, Any]:
    if isinstance(obj_in, dict):
        return obj_in
    return obj_in.model_dump(exclude_unset=True)


class BaseRepo(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    model: Type[ModelT]

    def __init__(self, model: Type[ModelT]):
        self.model = model

    async def callback_create(
        self, db_obj: ModelT, *, deps: StructuredCommonDeps
    ) -> None:
        """
        Callback after entity creation. Use this to add a background task to update the FGA tuples.
        """
        raise NotImplementedError()

    async def callback_delete(
        self, db_obj: ModelT, *, deps: StructuredCommonDeps
    ) -> None:
        """
        Callback after entity deletion. Use this to add a background task to update the FGA tuples.
        """
        raise NotImplementedError()

    async def callback_update(
        self, db_obj: ModelT, *, deps: StructuredCommonDeps
    ) -> None:
        """
        Callback after entity update. Useful for updating search indexes.
        """

    async def get(self, session: AsyncSession, id_: Any) -> ModelT:
        stmt = select(self.model).where(self.model.id == id_)
        res = await session.exec(stmt)
        db_obj = res.first()
        if db_obj is None:
            raise NotFoundException(self.model.__name__.lower())
        return db_obj

    async def create(
        self,
        deps: StructuredCommonDeps,
        *,
        obj_in: CreateSchemaT,
    ) -> ModelT:
        db_obj = cast(ModelT, self.model(**obj_in.model_dump()))
        session = deps.session
        session.add(db_obj)
        try:
            await session.commit()
        except Exception as exc:
            await session.rollback()
            raise exc
        await session.refresh(db_obj)
        await self.callback_create(db_obj, deps=deps)
        return db_obj

    async def update(
        self,
        deps: StructuredCommonDeps,
        *,
        id_: int,
        obj_in: UpdateSchemaOrDict[UpdateSchemaT],
    ) -> ModelT:
        update_data = get_dict_from_obj_in_update(obj_in)
        session = deps.session
        db_obj = await self.get(session, id_)
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        try:
            await session.commit()
        except Exception as exc:
            await session.rollback()
            raise exc
        await session.refresh(db_obj)
        await self.callback_update(db_obj, deps=deps)
        return db_obj

    async def remove(
        self,
        deps: StructuredCommonDeps,
        *,
        id_: int,
    ) -> None:
        session = deps.session
        obj = await self.get(session, id_)
        await session.delete(obj)
        try:
            await session.commit()
            await self.callback_delete(obj, deps=deps)
        except Exception as exc:
            await session.rollback()
            raise exc
