import os
from dotenv import load_dotenv
from src.pubsub.handlers import *

load_dotenv()

environment_variables_list: list = list(os.environ.keys())
environment_variables_dict: dict = {
    env_var: os.getenv(env_var) for env_var in environment_variables_list
}
post_ids: list[str] = []

for variable_name, variable_value in environment_variables_dict.items():
    if not variable_value:
        raise RuntimeError(f"{variable_name} is not set!")

POST_DELETED_TOPIC: str = environment_variables_dict["POST_DELETED_TOPIC"]
POST_CREATED_TOPIC: str = environment_variables_dict["POST_CREATED_TOPIC"]
LIST_ALL_POSTS_TOPIC: str = environment_variables_dict["LIST_ALL_POSTS_TOPIC"]

TOPICS: list = [POST_DELETED_TOPIC, POST_CREATED_TOPIC, LIST_ALL_POSTS_TOPIC]

HANDLERS_MAP = {
    POST_DELETED_TOPIC: post_deleted_handler,
    POST_CREATED_TOPIC: post_created_handler,
    LIST_ALL_POSTS_TOPIC: list_all_posts_handler

}


def set_connection_string(connection_string: str) -> str:
    for env_variable in environment_variables_list:
        if env_variable in connection_string:
            connection_string = connection_string.replace(env_variable, environment_variables_dict[env_variable])
    return connection_string
