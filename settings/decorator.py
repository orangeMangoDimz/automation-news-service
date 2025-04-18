from time import time, sleep


def retry(max_attempt: int = 5, delay: int = 3, exec_msg: str = "Function"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempt):
                try:
                    now = time()
                    func(*args, **kwargs)
                    return print(f"{exec_msg} takes ", time() - now)
                except Exception as e:
                    print(f"Attempt Failed #{attempt}")
                    print(f"Traceback: {e}")
                    print("Retry ...")
                    sleep(delay)
            raise RuntimeError(f"Max retries ({max_attempt}) exceeded.")

        return wrapper

    return decorator
