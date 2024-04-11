from app.common.deps.search import StructuredSearchClient
from app.common.search import meili_search_client
from app.user.search import UserSearch


def get_test_indexes(worker_id):
    user_index = f"test_{UserSearch.index_name}_{worker_id}"

    return user_index


def get_test_search_clients(worker_id) -> StructuredSearchClient:
    user_index = get_test_indexes(worker_id)

    user_search = UserSearch(index_name=user_index)

    return StructuredSearchClient(
        user=user_search,
    )


def delete_search_indexes(worker_id):
    user_index = get_test_indexes(worker_id)

    meili_search_client.delete_index(user_index)
