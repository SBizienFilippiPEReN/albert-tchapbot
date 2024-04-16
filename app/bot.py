# SPDX-FileCopyrightText: 2023 Pôle d'Expertise de la Régulation Numérique <contact.peren@finances.gouv.fr>
#
# SPDX-License-Identifier: MIT
from matrix_bot.bot import MatrixBot
from commands import command_registry
from config import env_config
from matrix_bot.config import logger


def main():
    tchap_bot = MatrixBot(
        env_config.matrix_home_server,
        env_config.matrix_bot_username,
        env_config.matrix_bot_password,
    )
    for callback in [
        feature
        for feature_group in env_config.groups_used
        for feature in command_registry.activate_and_retrieve_group(feature_group)
    ]:
        logger.info("loaded feature", feature=callback.__name__)
        tchap_bot.callbacks.register_on_message_event(callback, tchap_bot.matrix_client)
    tchap_bot.run()
