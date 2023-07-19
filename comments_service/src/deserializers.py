from src.database_models import PyObjectId


def post_deserializer(post: dict) -> PyObjectId:
    return PyObjectId(post['id'])
