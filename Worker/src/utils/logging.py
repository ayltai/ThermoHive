def log_debug(message: str) -> None:
    print(f'[DEBUG] {message}')


def log_error(e: Exception) -> None:
    print(f'[ERROR] {type(e).__name__}: {e}')

    raise e
