from datetime import datetime, timedelta

from django.http import HttpResponseBadRequest


def post_request(f):
    def wrapper(request):
        wrapper.__name__ = f.__name__
        if request.is_ajax() or request.method == 'POST':
            return f(request)
        return HttpResponseBadRequest

    return wrapper


def dates_filter(f):

    date_format = "%m/%d/%Y"

    def wrapper(request):
        nonlocal date_format

        now = datetime.now()
        five_days_ago = now - timedelta(days=5)

        start_date = request.POST.get('start_date', five_days_ago)
        end_date = request.POST.get('end_date', now)

        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, date_format)

        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, date_format)

        if start_date > end_date:
            end_date = start_date - timedelta(days=1)

        return f(start_date.date(), end_date.date())

    return wrapper

