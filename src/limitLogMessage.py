def limit_log_message(message, max_length=100, truncation_indicator='... [truncated]'):
    """
    Truncate a message to a specified length, adding a truncation indicator if necessary.

    Args:
        message (str or list): The message to be truncated.
        max_length (int, optional): Maximum allowed length of the message. Defaults to 100.
        truncation_indicator (str, optional): Indicator to append if truncation occurs. Defaults to '... [truncated]'.

    Returns:
        str: The truncated message if necessary, otherwise the original message.
    """
    if isinstance(message, list):
        message = ', '.join(map(str, message))

    if isinstance(message, str):
        return message if len(message) <= max_length else message[:max_length] + truncation_indicator

    return "Invalid input type. Expected str or list."
