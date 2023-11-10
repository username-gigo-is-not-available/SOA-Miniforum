def notification_not_created_message() -> str:
    return "Unable to create notification!"


def notification_not_found_message(notification_id: str) -> str:
    return f"Notification {notification_id} not found!"


def empty_inbox_message() -> str:
    return f"Empty inbox!"
