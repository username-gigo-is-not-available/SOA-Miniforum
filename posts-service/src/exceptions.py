from src.database_models import Post


def user_has_not_posted_yet_message(user_id: int):
    return f"User with user_id {user_id} has not posted yet!"


def no_active_posts_message():
    return f"There are no active posts. Start the conversation by creating the first post.!"


def post_not_found_message(post_id: str):
    return f"Post with {post_id} was not found!"


def post_has_no_comments_message(post_id: str):
    return f"Post with post_id {post_id} has no comments!"


def count_posts_by_user_message(user_id: int, total_posts: int):
    return f"User with {user_id} has total of {total_posts} posts!"


def posts_by_user_message(user_id: int, posts: list[Post]):
    return f"Posts by user with user_id: {user_id} {posts}."


def post_has_total_comments_message(post_id: str, total_comments: int):
    return f"Post with {post_id} has total of {total_comments}"


def post_not_created_message():
    return f"Unable to create post!"
