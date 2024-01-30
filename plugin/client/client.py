from dataclasses import dataclass, field
from cloudquery.sdk.scheduler import Client as ClientABC

from plugin.formations.formation import FormationClient


DEFAULT_CONCURRENCY = 100
DEFAULT_QUEUE_SIZE = 10000


@dataclass
class Spec:
    username: str = field(default=None)
    password: str = field(default=None)
    base_url: str = field(default="https://api.example.com")
    concurrency: int = field(default=DEFAULT_CONCURRENCY)
    queue_size: int = field(default=DEFAULT_QUEUE_SIZE)

    def validate(self):
        pass
        # if self.access_token is None:
        #     raise Exception("access_token must be provided")


class FormationsClient(ClientABC):
    def __init__(self, spec: Spec) -> None:
        self._spec = spec
        self._client = FormationClient(spec.username, spec.password)

    def id(self):
        return "example"

    @property
    def client(self) -> FormationClient:
        return self._client
