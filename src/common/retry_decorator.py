import asyncio
import functools
import time
from typing import Callable, Any, Union

def retry(max_retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries):
                try:
                    print(f"Attempt {attempt + 1}/{max_retries} for {func.__name__}")
                    result = func(*args, **kwargs)
                    print(f"Success on attempt {attempt + 1} for {func.__name__}")
                    return result
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}")
                    if attempt == max_retries - 1:
                        print(f"All {max_retries} attempts exhausted for {func.__name__}")
                        raise
                    print(f"Waiting {delay} seconds before next retry...")
                    time.sleep(delay)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries):
                try:
                    print(f"Attempt {attempt + 1}/{max_retries} for {func.__name__}")
                    result = await func(*args, **kwargs)
                    print(f"Success on attempt {attempt + 1} for {func.__name__}")
                    return result
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}")
                    if attempt == max_retries - 1:
                        print(f"All {max_retries} attempts exhausted for {func.__name__}")
                        raise
                    print(f"Waiting {delay} seconds before next retry...")
                    await asyncio.sleep(delay)

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator
