from typing import Any, Generator

import pyarrow as pa
from cloudquery.sdk.scheduler import TableResolver
from cloudquery.sdk.schema import Column
from cloudquery.sdk.schema import Table
from cloudquery.sdk.schema.resource import Resource

from plugin.client import FormationsClient
from plugin.tables.plans import Plans


class Deployments(Table):
    def __init__(self) -> None:
        super().__init__(
            name="deployments",
            title="Deployments",
            columns=[
                Column("id", pa.string(), primary_key=True),
                Column("environment", pa.string()),
                Column("role", pa.string()),
                Column("active", pa.bool_()),
                Column("description", pa.string()),
            ],
            relations=[Plans()],
        )

    @property
    def resolver(self):
        return DeploymentResolver(table=self)


class DeploymentResolver(TableResolver):
    def __init__(self, table=None) -> None:
        super().__init__(table=table)

    def resolve(
        self, client: FormationsClient, parent_resource: Resource
    ) -> Generator[Any, None, None]:
        for deployment_response in client.client.deployment_iterator():
            yield deployment_response

    @property
    def child_resolvers(self):
        return [table.resolver for table in self._table.relations]