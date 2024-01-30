from typing import Any, Generator

import pyarrow as pa
from cloudquery.sdk.scheduler import TableResolver
from cloudquery.sdk.schema import Column
from cloudquery.sdk.schema import Table
from cloudquery.sdk.schema.resource import Resource

from plugin.client import FormationsClient


class Formations(Table):
    def __init__(self) -> None:
        super().__init__(
            name="formations",
            title="Formations",
            columns=[
                Column("id", pa.string()),
                Column("name", pa.string()),
                Column("environment", pa.string()),
                Column("role", pa.string()),
                Column("realm", pa.string()),
                Column("world", pa.string()),
                Column("instance_type", pa.string()),
                Column("instance_count", pa.int64()),
                Column("active", pa.bool_()),
            ],
        )

    @property
    def resolver(self):
        return FormationResolver(table=self)


class FormationResolver(TableResolver):
    def __init__(self, table) -> None:
        super().__init__(table=table)

    def resolve(
        self, client: FormationsClient, parent_resource: Resource
    ) -> Generator[Any, None, None]:
        for formation_response in client.client.formation_iterator():
            yield formation_response
