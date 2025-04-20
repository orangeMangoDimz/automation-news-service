from time import sleep
from typing import Optional
from settings import AppLogger


def retry(
    max_attempt: int = 5,
    delay: int = 3,
    exec_msg: str = "Function",
    logger: Optional[AppLogger] = None,
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal logger
            last_exception: Exception | None = None

            if logger is None and args:
                instance = args[0]
                if hasattr(instance, "logger"):
                    logger = getattr(instance, "logger")

            for attempt in range(max_attempt):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception: Exception | None = e
                    attempt_number: int = attempt + 1
                    error_msg: str = (
                        f"{exec_msg} attempt failed (#{attempt_number}/{max_attempt}). "
                        f"Error: {str(e)}"
                    )

                    if logger:
                        # Log with different levels based on attempt number
                        if attempt_number == max_attempt:
                            logger.error(error_msg)
                        else:
                            logger.warning(error_msg)

                        # Only log traceback on final attempt to avoid noise
                        if attempt_number == max_attempt:
                            logger.exception("Full traceback:")
                    else:
                        # Fallback to print if no logger provided
                        print(error_msg)
                        if attempt_number == max_attempt:
                            import traceback

                            traceback.print_exc()

                    if attempt_number < max_attempt:
                        sleep(delay)

            raise RuntimeError(
                f"Max retries ({max_attempt}) exceeded for {exec_msg}"
            ) from last_exception

        return wrapper

    return decorator
