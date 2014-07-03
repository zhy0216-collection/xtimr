from functools import wraps


import ujson
from django.http import HttpResponse


def to_json(f):
    @wraps(f)
    def _decorator_func(*args, **kwargs):
        result = f(*args, **kwargs)
        return HttpResponse(ujson.dumps(result),
                            content_type="application/json"
               )
    return _decorator_func

def require_login(f):
    pass



