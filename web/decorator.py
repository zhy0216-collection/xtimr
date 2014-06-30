from funtools import wrap


import ujson
from django.http import HttpResponse


def to_json(f):
    @wrap
    def _decorator_func(*args, *kwargs):
        result = f(*args, *kwargs)
        return HttpResponse(ujson.dumps(result),
                            content_type="application/json"
               )
    return _decorator_func

def require_login(f):
    pass



