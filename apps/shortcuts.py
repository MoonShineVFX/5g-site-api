# -*- coding: utf-8 -*-
import uuid
import functools
import time

from django.utils import timezone
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection, reset_queries


utc_now = timezone.now()


def get_or_404(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404('No object matches the given ID.')
    return wrapper


def validate_pk(str):
    try:
        obj_id = uuid.UUID(str)
    except (TypeError, ValueError):
        raise Http404('ID format is wrong.')
    return obj_id


@get_or_404
def select_data_or_404(obj, str_id, *args, **kwargs):
    obj_id = validate_pk(str_id)
    if args or kwargs:
        if len(args) == 1:
            return obj.objects.values_list(*args, flat=True).filter(id=obj_id, **kwargs)
        else:
            return obj.objects.values_list(*args).filter(id=obj_id, **kwargs)
    else:
        return obj.objects.get(id=obj_id)


@get_or_404
def update_data_or_404(obj, str_id, *args, **kwargs):
    obj_id = validate_pk(str_id)
    obj.objects.filter(id=obj_id).update(*args, **kwargs)


def debugger_queries(func):
    """Basic function to debug queries."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("func: ", func.__name__)
        reset_queries()

        start = time.time()
        start_queries = len(connection.queries)

        result = func(*args, **kwargs)

        end = time.time()
        end_queries = len(connection.queries)

        print("queries:", end_queries - start_queries)
        print("took: %.2fs" % (end - start))
        return result

    return wrapper

