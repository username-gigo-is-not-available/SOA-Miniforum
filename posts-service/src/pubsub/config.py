from src.pubsub.handlers import user_created_handler, user_deleted_handler, list_all_users_handler
from src.settings import environment_variables_dict

POST_DELETED_TOPIC: str = environment_variables_dict["POST_DELETED_TOPIC"]
POST_CREATED_TOPIC: str = environment_variables_dict["POST_CREATED_TOPIC"]
LIST_ALL_POSTS_TOPIC: str = environment_variables_dict["LIST_ALL_POSTS_TOPIC"]

USER_CREATED_TOPIC: str = environment_variables_dict["USER_CREATED_TOPIC"]
LIST_ALL_USERS_TOPIC: str = environment_variables_dict["LIST_ALL_USERS_TOPIC"]
USER_DELETED_TOPIC: str = environment_variables_dict["USER_DELETED_TOPIC"]


TOPICS: list = [POST_DELETED_TOPIC, POST_CREATED_TOPIC, LIST_ALL_POSTS_TOPIC, USER_CREATED_TOPIC, USER_DELETED_TOPIC,
                LIST_ALL_USERS_TOPIC]

HANDLERS_MAP = {
    USER_CREATED_TOPIC: user_created_handler,
    USER_DELETED_TOPIC: user_deleted_handler,
    LIST_ALL_USERS_TOPIC: list_all_users_handler,
}