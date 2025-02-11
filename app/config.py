# SPDX-FileCopyrightText: 2023 Pôle d'Expertise de la Régulation Numérique <contact.peren@finances.gouv.fr>
# SPDX-FileCopyrightText: 2024 Etalab/Datalab <etalab@modernisation.gouv.fr>
#
# SPDX-License-Identifier: MIT

import logging
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PACKAGE_PATH = Path(__file__).resolve().parent
SRC_PATH = PACKAGE_PATH.parent
_ROOT_PATH = PACKAGE_PATH.parent.parent  # Accessible from clone of the project, not from package
DOCUMENTATION_DIR = _ROOT_PATH / "docs"
README_PATH = _ROOT_PATH / "README.md"

COMMAND_PREFIX = "!"


class BaseConfig(BaseSettings):
    # allows us to clean up the imports into multiple parts
    # https://stackoverflow.com/questions/77328900/nested-settings-with-pydantic-settings
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent / ".env", extra="ignore"
    )  # allows nested configs


class Config(BaseConfig):
    verbose: bool = Field(False, description="Enable / disable verbose logging")
    systemd_logging: bool = Field(
        True, description="Enable / disable logging with systemd.journal.JournalHandler"
    )
    matrix_home_server: str = Field(
        "https://matrix.agent.dinum.tchap.gouv.fr", description="Tchap home server URL"
    )
    matrix_bot_username: str = Field("", description="username of our matrix bot")
    matrix_bot_password: str = Field("", description="password of our matrix bot")
    groups_used: list[str] = Field(["basic"], description="List of commands groups to use")
    albert_api_url: str = Field("http://localhost:8090/api/v2", description="Albert API base URL")
    albert_api_token: str = Field("", description="Albert API TOKEN")

    # Conversational settings
    with_history: bool = Field(True, description="Conversational mode")
    chat_id: int|None = Field(None, description="Current chat id")


env_config = Config()


def use_systemd_config():
    if not env_config.systemd_logging:
        return

    from systemd import journal

    # remove the default handler, if already initialized
    existing_handlers = logging.getLogger().handlers
    for handlers in existing_handlers:
        logging.getLogger().removeHandler(handlers)
    # Sending logs to systemd-journal if run via systemd, printing out on console otherwise.
    logging_handler = (
        journal.JournalHandler() if env_config.systemd_logging else logging.StreamHandler()
    )
    logging.getLogger().addHandler(logging_handler)
