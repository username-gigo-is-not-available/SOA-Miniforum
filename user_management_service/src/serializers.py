from src.database_models import User


def user_serializer(user: User) -> dict:
    data = user.dict()
    data['timestamp'] = int(data['timestamp'].timestamp())
    return data
