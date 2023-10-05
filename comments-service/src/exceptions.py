from src.database_models import Comment


def comment_not_found_message(comment_id: str):
    return f"Comment with {comment_id} was not found!"


def comments_not_found_message():
    return "No comments found!"


def user_has_not_commented_yet_message(user_id: int):
    return f"User with user_id {user_id} has not commented yet!"


def comments_by_user_message(user_id: int, comments: list[Comment]):
    return f"Comments by user with user_id: {user_id} {comments}."


def total_comments_by_user_message(user_id: int, total_comments: int):
    return f"User with {user_id} has total of {total_comments} comments!"


def post_has_comments_message(post_id: str, comments: list[Comment]):
    return f"Post with post_id has comments: {post_id} {comments}."


def post_not_found_message(post_id: str):
    return f"Post with {post_id} was not found!"


def post_has_no_comments_message(post_id: str):
    return f"Post with post_id {post_id} has no comments!"


def post_has_total_comments_message(post_id: str, total_comments: int):
    return f"Post with {post_id} has total of {total_comments}"


def comment_not_created_message():
    return f"Unable to create comment!"
