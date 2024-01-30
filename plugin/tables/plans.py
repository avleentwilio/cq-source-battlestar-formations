from typing import Any, Generator

import pyarrow as pa
from cloudquery.sdk.scheduler import TableResolver
from cloudquery.sdk.schema import Column
from cloudquery.sdk.schema import Table
from cloudquery.sdk.schema.resource import Resource

from plugin.client import FormationsClient


class Plans(Table):
    def __init__(self) -> None:
        super().__init__(
            name="plans",
            title="Plans",
            columns=[
                Column("formation_id", pa.string(), primary_key=True),
                Column("formation_type", pa.string()),
                Column("deployment_id", pa.string()),
                Column("manifest", pa.string()),
                Column("manifest_type", pa.string()),
                Column("configuration", pa.string()),
            ],
        )

    @property
    def resolver(self):
        return PlansResolver(table=self)


class PlansResolver(TableResolver):
    def __init__(self, table) -> None:
        super().__init__(table=table)

    def resolve(
        self, client: FormationsClient, parent_resource: Resource
    ) -> Generator[Any, None, None]:
        for plan in parent_resource.item["plans"]:
            yield plan
