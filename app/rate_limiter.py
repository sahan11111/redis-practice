import redis
from rest_framework.exceptions import Throttled

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

def rate_limit(max_requests: int, time_window: int):
    def decorator(view_func):
        def wrapper(self, request, *args, **kwargs):

            if request.user.is_authenticated:
                identifier = f"user:{request.user.id}"
            else:
                identifier = f"ip:{request.META.get('REMOTE_ADDR')}"

            key = f"rate:{identifier}:{request.path}"

            current = redis_client.incr(key)

            if current == 1:
                redis_client.expire(key, time_window)

            if current > max_requests:
                retry_after = redis_client.ttl(key)
                raise Throttled(
                    detail="Rate limit exceeded. Try again later.",
                    wait=retry_after
                )

            return view_func(self, request, *args, **kwargs)

        return wrapper
    return decorator
