import requests

from typing import Generator, Dict, Any


class FormationClient:
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def deployment_iterator(self, page: int = 1) -> Generator[Dict[str, Any], None, None]:
        url = "https://battlestar.corp.twilio.com/v1/Deployments"
        while True:
            response = requests.get(url, auth=(self._username, self._password), params={'page_size': 1000})
            if response.status_code != 200:
                raise ValueError(f"Failed to get deployments: {response.text}")
            try:
                payload = response.json()
            except requests.exceptions.JSONDecodeError:
                raise ValueError(f"Failed to decode deployments response: {response.text}")
            if not payload.get("items"):
                print("No deployments found in: {}".format(payload))
            for deployment in payload["items"]:
                # Skip if the environment is not production
                if deployment["environment"] != "prod":
                    continue

                plans = []
                for plan_response in deployment["plans"]:
                    plans.append({
                        "formation_id": plan_response["formation"],
                        "formation_type": plan_response["formation_type"],
                        "deployment_id": deployment["id"],
                        "manifest": plan_response["manifest"],
                        "manifest_type": plan_response["manifest_type"],
                    })
                try:
                    result = {
                        "id": deployment["id"],
                        "environment": deployment["environment"],
                        "role": deployment["role"],
                        "active": deployment["active"],
                        "description": deployment["description"],
                        "plans": plans,
                    }
                except KeyError:
                    print("KeyError in deployment: {}".format(deployment))
                    continue
                yield result
            if payload.get("meta").get("next"):
                url = payload["meta"]["next"]
            else:
                break

    def formation_iterator(self, page: int = 1) -> Generator[Dict[str, Any], None, None]:
        url = "https://battlestar.corp.twilio.com/v1/Formations/AWS"
        while True:
            response = requests.get(url, auth=(self._username, self._password), params={'page_size': 1000})
            if response.status_code != 200:
                raise ValueError(f"Failed to get formations: {response.text}")
            try:
                payload = response.json()
            except requests.exceptions.JSONDecodeError:
                raise ValueError(f"Failed to decode formations response: {response.text}")
            if not payload.get("items"):
                print("No formations found in: {}".format(payload))
            for formation in payload["items"]:
                for realm in formation["realms"]:
                    # Skip if the environment is not production
                    if formation["environment"] != "prod":
                        continue

                    try:
                        result = {
                            "id": formation["id"],
                            "name": formation["name"],
                            "environment": formation["environment"],
                            "role": formation["role"],
                            "realm": realm,
                            "world": formation["realms"][realm]["world"],
                            "instance_type": formation["realms"][realm]["instance_type"],
                            "instance_count": formation["realms"][realm]["instance_count"],
                            "active": formation["active"],
                        }
                    except KeyError:
                        print("KeyError in formation: {}".format(formation))
                        continue
                    yield result
            if payload.get("meta").get("next"):
                url = payload["meta"]["next"]
            else:
                break
