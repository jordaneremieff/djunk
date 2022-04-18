from pathlib import Path

import djclick as click

from django.core import management
from django.conf import settings


@click.command()
@click.argument("name")
def command(name: str):
    template = str(Path(__file__).resolve().parent / "app_template")

    # Creates the app under `djunk/apps/` instead of the project root.
    target = settings.APPS_DIR / name
    target.mkdir(parents=True, exist_ok=True)
    management.call_command("startapp", name, target, template=template)
    click.secho(
        f"New app {name} succesfully created! \nAppend 'djunk.apps.{name}' to "
        "the `INSTALLED_APPS` in the settings to enable it."
    )
