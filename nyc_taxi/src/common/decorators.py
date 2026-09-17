from functools import wraps
import time
def log_execution(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.time()

        try:
            result = func(*args, **kwargs)

            duration = round(time.time() - start, 2)

            self = args[0]

            self.logger.info(
                f"{func.__name__} completed "
                f"in {duration}s"
            )

            return result

        except Exception as e:

            self = args[0]

            self.logger.error(str(e))
            raise

    return wrapper

