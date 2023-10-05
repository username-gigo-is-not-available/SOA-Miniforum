from src.database_models import Post, PyObjectId


def post_serializer(post: Post) -> dict:
    data = post.dict()
    data['timestamp'] = int(data['timestamp'].timestamp())
    data['id'] = str(post.id)
    return data
