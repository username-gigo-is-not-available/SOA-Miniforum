from src.pubsub.handlers import post_deleted_handler, post_created_handler, list_all_posts_handler
from src.settings import environment_variables_dict

POST_DELETED_TOPIC: str = environment_variables_dict["POST_DELETED_TOPIC"]
POST_CREATED_TOPIC: str = environment_variables_dict["POST_CREATED_TOPIC"]
LIST_ALL_POSTS_TOPIC: str = environment_variables_dict["LIST_ALL_POSTS_TOPIC"]

TOPICS: list = [POST_DELETED_TOPIC, POST_CREATED_TOPIC, LIST_ALL_POSTS_TOPIC]

HANDLERS_MAP = {
    POST_DELETED_TOPIC: post_deleted_handler,
    POST_CREATED_TOPIC: post_created_handler,
    LIST_ALL_POSTS_TOPIC: list_all_posts_handler

}

