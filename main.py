import httpx
import time
import paho.mqtt.publish as publish
import datetime
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    mqtt_hostname: str
    mqtt_user: str
    mqtt_password: str | None = None
    coffeelog_api: str
    users: list[str] = []

settings = Settings()


def read_total(auth: dict[str, str | None]) -> None:
    """Publish the total amount of coffee."""
    r = httpx.get(f"{settings.coffeelog_api}/actions/count/total")
    if r.status_code == 200:
        if type(r.json()) == int:
            publish.single(
                "iot/coffee/count",
                r.json(),
                hostname=settings.mqtt_hostname,
                auth=auth,
            )
            publish.single(
                "iot/coffee/count/total",
                r.json(),
                hostname=settings.mqtt_hostname,
                auth=auth,
            )


def read_total_user(auth: dict[str, str | None], user: str) -> None:
    """Publish the total amount of coffee per user."""
    r = httpx.get(f"{settings.coffeelog_api}/actions/count/total/{user}")
    if r.status_code == 200:
        if type(r.json()) == int:
            publish.single(
                f"iot/coffee/count/total/{user}",
                r.json(),
                hostname=settings.mqtt_hostname,
                auth=auth,
            )


def read_total_today(auth: dict[str, str | None]) -> None:
    """Publish the total amount of coffee of today."""
    r = httpx.get(f"{settings.coffeelog_api}/actions/count/today")
    if r.status_code == 200:
        if type(r.json()) == int:
            publish.single(
                f"iot/coffee/count/today",
                r.json(),
                hostname=settings.mqtt_hostname,
                auth=auth,
            )


def read_total_today_user(auth: dict[str, str | None], user: str) -> None:
    """Publish the total amount of coffee of today per given user."""
    r = httpx.get(f"{settings.coffeelog_api}/actions/count/today/{user}")
    if r.status_code == 200:
        if type(r.json()) == int:
            publish.single(
                f"iot/coffee/count/today/{user}",
                r.json(),
                hostname=settings.mqtt_hostname,
                auth=auth,
            )


def read_loaded_coffee(auth: dict[str, str | None]):
    """Publish the information about the coffee set up in the machine."""
    r = httpx.get(f"{settings.coffeelog_api}/coffee/latest")
    if r.status_code == 200:
        data = r.json()
        publish.single(
            f"iot/coffee/loaded/coffee",
            data["coffee_name"],
            hostname=settings.mqtt_hostname,
            auth=auth,
        )
        publish.single(
            f"iot/coffee/loaded/roasting_facility",
            data["roasting_facility"],
            hostname=settings.mqtt_hostname,
            auth=auth,
        )
        publish.single(
            f"iot/coffee/loaded/country_of_origin",
            data["country_of_origin"],
            hostname=settings.mqtt_hostname,
            auth=auth,
        )
        publish.single(
            f"iot/coffee/loaded/open_date",
            data["open_date"],
            hostname=settings.mqtt_hostname,
            auth=auth,
        )
        publish.single(
            f"iot/coffee/loaded/roast_date",
            data["roast_date"],
            hostname=settings.mqtt_hostname,
            auth=auth,
        )


if __name__ == "__main__":
    auth = {'username': settings.mqtt_user, 'password': settings.mqtt_password}
    users = settings.users

    while True:
        read_total(auth)
        read_total_today(auth)
        read_loaded_coffee(auth)
        for user in users:
            read_total_user(auth, user)
            read_total_today_user(auth, user)

        print(f"{datetime.datetime.now()}: read")
        time.sleep(1)
