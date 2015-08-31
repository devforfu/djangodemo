import json
from datetime import datetime
from operator import itemgetter

from django.shortcuts import render
from django.http import HttpResponse

from welcome.utils import dates_filter, post_request
from welcome.insights import open_tickets_count
from welcome.insights import avg_reply_time, avg_ticket_close_time
from welcome.insights import open_tickets_chart, reply_moving_average


def home_page(request):
    if request.is_ajax() or request.method == 'POST':
        return HttpResponse("AJAX request handled")

    return render(request, 'index.html')


@post_request
@dates_filter
def bar_chart(start_date, end_date):
    chart = open_tickets_chart(start_date, end_date)

    if not chart:
        return HttpResponse('{"result": []}')

    pairs = sorted(chart.items(), key=itemgetter(0))
    result = {'result': [{'date': k.strftime("%m/%d/%Y"), 'val': v}
                         for k, v in pairs]}

    json_response = json.dumps(result)

    return HttpResponse(json_response)


@post_request
@dates_filter
def users(start_date, end_date):
    chart = reply_moving_average(start_date, end_date).to_dict(orient='list')

    if not chart:
        return HttpResponse('{"result": []}')

    pairs = zip(sorted(chart['date']), chart['avg'])
    result = {"result": [{"date": k.strftime("%m/%d/%Y"), "DAU": v}
                         for k, v in pairs]}

    json_response = json.dumps(result)

    return HttpResponse(json_response)


@post_request
def open_tickets(request):
    count = open_tickets_count()
    json.dumps({"result": })
    return HttpResponse("{} days".format(count))


@post_request
def avg_reply_time(request):
    avg = avg_reply_time()
    response = "Not available" if not avg else str(avg) + " days"
    return HttpResponse(response)


@post_request
def avg_ticket_close_time(request):
    avg = avg_ticket_close_time()
    response = "Not available" if not avg else str(avg) + " days"
    return HttpResponse(response)
