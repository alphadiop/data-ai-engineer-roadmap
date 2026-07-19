from functools import wraps
import time

def log_execution(func):

    @wraps(func)
    def wrapper(self, context, *args, **kwargs):

        start = time.time()

        try:

            result = func(
                self,
                context,
                *args,
                **kwargs
            )

            duration = round(time.time() - start,2)

            self.logger.info(
                f"{func.__name__} completed "
                f"in {duration}s"
            )
            return result

        except Exception as e:

            context.status = "ERROR"
            context.message = str(e)
            context.row_count["silver"] = 0
            self.logger.error(str(e))
            raise
    return wrapper