import json
import time
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    TypedDict,
    TypeVar,
    cast,
    Iterable,
)

import meilisearch
from meilisearch.errors import MeilisearchApiError
from meilisearch.index import Index
from meilisearch.models.task import Task

from app.core.config import settings

meili_search_client = meilisearch.Client(settings.MEILI_URL, settings.MEILI_MASTER_KEY)
ModelT = TypeVar("ModelT", bound=Any)


class SearchResultT(TypedDict):
    hits: List[Dict[str, Any]]
    query: str
    processingTimeMs: int
    limit: int
    offset: int
    estimatedTotalHits: int


class MeiliSearchBaseClass(Generic[ModelT]):
    index: Index
    index_name: str = ""
    sortable_attributes: List[str] = []
    filterable_attributes: List[str] = []

    def __init__(self, index_name: Optional[str] = None) -> None:
        if index_name:
            self.index_name = index_name
        try:
            self.create_index()
        except MeilisearchApiError:
            pass
        self.index = meili_search_client.get_index(self.index_name)

        if self.index.get_filterable_attributes() != self.filterable_attributes:
            self.index.update_filterable_attributes(self.filterable_attributes)
        if self.index.get_sortable_attributes() != self.sortable_attributes:
            self.index.update_sortable_attributes(self.sortable_attributes)

    def create_index(self) -> None:
        task_info = meili_search_client.create_index(
            self.index_name, {"primaryKey": "id"}
        )
        task_uid = task_info.task_uid
        status = task_info.status

        while status in ["enqueued", "processing"]:
            time.sleep(0.01)
            task = self.get_task(task_uid)
            status = task.status

    @staticmethod
    def get_task(task_id: int) -> Task:
        return meili_search_client.get_task(task_id)

    @staticmethod
    def get_formatted_documents(objs_in: Iterable[ModelT]) -> List[Dict[str, Any]]:
        return [json.loads(obj_in.model_dump_json()) for obj_in in objs_in]

    def search(
        self, query: str, opts: Optional[Dict[str, Any]] = None
    ) -> SearchResultT:
        opts = opts or {}
        return cast(SearchResultT, self.index.search(query, opts))

    def add_documents(self, entities: Iterable[ModelT]) -> Task:
        documents = self.get_formatted_documents(entities)
        task_info = self.index.add_documents(documents)
        task_uid = task_info.task_uid
        status = task_info.status
        task = self.get_task(task_uid)

        while status in ["enqueued", "processing"]:
            time.sleep(0.01)
            task = self.get_task(task_uid)
            status = task.status

        return task

    def update_documents(self, entities: Iterable[ModelT]) -> Task:
        documents = self.get_formatted_documents(entities)
        task_info = self.index.update_documents(documents)
        task_uid = task_info.task_uid
        status = task_info.status
        task = self.get_task(task_uid)

        while status in ["enqueued", "processing"]:
            time.sleep(0.01)
            task = self.get_task(task_uid)
            status = task.status

        return task

    def delete_document(self, entity: ModelT) -> Task:
        task_info = self.index.delete_document(entity.id)
        task_uid = task_info.task_uid
        status = task_info.status
        task = self.get_task(task_uid)

        while status in ["enqueued", "processing"]:
            time.sleep(0.01)
            task = self.get_task(task_uid)
            status = task.status

        return task
