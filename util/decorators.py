from datetime import datetime, timedelta


def cache_result(secs=30):
    '''Cache result and use it for number of secs from the time it was cached'''
    def real_decorator(func):
        # Will store cache in this var
        cache = {}
        def wrapper(*args):
            expire_cache()

            if args in cache:
                return cache[args]['result']

            result = func(*args)
            cache[args] = {
                'created': datetime.utcnow(),
                'result': result
            }
            return result

        def expire_cache():
            timeborder = datetime.utcnow() - timedelta(seconds=secs)
            for k in cache.keys():
                if cache[k]['created'] < timeborder:
                    del cache[k]

        return wrapper
    return real_decorator