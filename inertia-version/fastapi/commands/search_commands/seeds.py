from typing import Sequence, Type, cast

from sqlmodel import Session, select

from app.core.sync_db import engine

from app.common.search import MeiliSearchBaseClass, ModelT
from app.user.models import User
from app.user.search import UserSearch

from commands.utils import import_all_models
from commands.print import print_info, print_success

import_all_models()

search_model_map = {UserSearch.index_name: User}


def seed_search_index(search_class: Type[MeiliSearchBaseClass[ModelT]]) -> None:
    print_info(f"Seeding {search_class.index_name} index")
    model_ = search_model_map[search_class.index_name]
    with Session(engine) as session:
        statement = select(model_)
        documents = cast(Sequence[ModelT], session.exec(statement).all())
        if len(documents) > 0:
            search_class().add_documents(documents)
    print_success(f"{search_class.index_name} index seeded successfully")
