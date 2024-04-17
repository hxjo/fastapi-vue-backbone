from sqlmodel import Session, select

from app.core.db import engine
from app.user.models import User
from app.user.search import UserSearch

from commands.utils import import_all_models
from commands.print import print_info, print_success

import_all_models()

search_model_map = {
    UserSearch.index_name: User
}


def seed_search_index(search_class):
    print_info(f"Seeding {search_class.index_name} index")
    model_ = search_model_map[search_class.index_name]
    with Session(engine) as session:
        statement = select(model_)
        documents = session.exec(statement).all()
        if len(documents) > 0:
            search_class().add_documents(documents)
    print_success(f"{search_class.index_name} index seeded successfully")
