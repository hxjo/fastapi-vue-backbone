from typing import Any, Dict, List, cast

from meilisearch.index import Index

from app.common.search import meili_search_client, MeiliSearchBaseClass
from app.user.models import User


class UserSearch(MeiliSearchBaseClass[User]):
    index_name: str = "users"
    index: Index = meili_search_client.index(index_name)
    filterable_attributes: List[str] = ["id"]

    @staticmethod
    def build_opts_with_filter(user_id: int) -> Dict[str, Any]:
        return {"filter": f"id != {user_id}"}

    def get_search_result_hits(
        self, query: str = "", offset: int = 0, *, current_user: User
    ) -> List[Dict[str, Any]]:
        opts = self.build_opts_with_filter(cast(int, current_user.id))
        opts.update({"offset": offset})
        search_results = self.search(query, opts)
        return search_results["hits"]
