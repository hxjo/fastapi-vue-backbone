from sqlalchemy import func
from sqlmodel import Session, select

from app.core.sync_db import engine
from app.user.search import UserSearch
from app.user.models import User
from commands.utils import import_all_models
from app.common.search import meili_search_client
from commands.print import print_success, print_warning

import_all_models()

index_model_map = {UserSearch.index_name: User}

index_name_search_map = {
    UserSearch.index_name: UserSearch,
}


def update_indexes_if_needed() -> None:
    stats = meili_search_client.get_all_stats()
    with Session(engine) as session:
        for index_name, index_value in stats["indexes"].items():
            number_of_documents = index_value["numberOfDocuments"]
            model_ = index_model_map[index_name]
            stmt = select(func.count()).select_from(model_)
            number_of_model_documents = session.exec(stmt).first()
            if number_of_documents != number_of_model_documents:
                print_warning(f"Updating {index_name} index")
                meili_search_client.index(index_name).delete()
                # seed_search_index(index_name_search_map[index_name])
                print_success(f"{index_name} index updated")
