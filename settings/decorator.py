from time import sleep


def retry(max_attempt: int = 5, delay: int = 3, exec_msg: str = "Function"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempt):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"{exec_msg} Attempt Failed #{attempt + 1}")
                    print(f"Traceback: {e}")
                    print(f"Retrying ({attempt + 1}/{max_attempt})...")
                    sleep(delay)
            raise RuntimeError(f"Max retries ({max_attempt}) exceeded.")

        return wrapper

    return decorator
