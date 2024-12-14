import time

def retry(function, retries=3, delay=2, *args, **kwargs):
    for attempt in range(retries):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e
