def limit_log_message(message, max_length=100):
    """
    Truncate a message to a specified length, adding a truncation indicator if necessary.
    
    Handles string and list inputs. If input is a list, it converts it to a string before truncating.
    """
    # Check if the message is a list
    if isinstance(message, list):
        # Join the list into a single string with a separator (e.g., comma)
        message = ', '.join(map(str, message))

    # Ensure the message is a string for processing
    if isinstance(message, str):
        return message if len(message) <= max_length else message[:max_length] + '... [truncated]'

    # If the message is not a string or list, return a default message or handle accordingly
    return "Invalid input type. Expected str or list."
