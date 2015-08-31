import json
from datetime import datetime
from operator import itemgetter

from django.shortcuts import render
from django.http import HttpResponse

import welcome.insights as insights
from welcome.utils import dates_filter, post_request
from welcome.insights import open_tickets_count
from welcome.insights import open_tickets_chart, reply_moving_average



def home_page(request):
    return render(request, 'index.html')


@post_request
@dates_filter
def bar_chart(start_date, end_date):
    chart = open_tickets_chart(start_date, end_date)

    if not chart:
        return HttpResponse('{"result": []}')

    pairs = zip(chart['date'], chart['count'])
    result = {'result': [{"date": k.strftime("%m/%d/%Y"), "val": v}
                         for k, v in pairs]}

    json_response = json.dumps(result)

    return HttpResponse(json_response)


@post_request
@dates_filter
def users(start_date, end_date):
    chart = reply_moving_average(start_date, end_date).to_dict(orient='list')

    if not chart:
        return HttpResponse('{"result": []}')

    pairs = zip(chart['date'], chart['avg'])
    result = {"result": [{"date": k.strftime("%m/%d/%Y"), "DAU": v}
                         for k, v in pairs]}

    json_response = json.dumps(result)

    return HttpResponse(json_response)


@post_request
def open_tickets(request):
    result = json.dumps({"result": str(open_tickets_count())})
    return HttpResponse(result)


@post_request
def avg_reply_time(request):
    avg = insights.avg_reply_time()
    response = "0" if not avg else "{0:.2f}".format(avg*24)
    result = json.dumps({"result": response + " "})
    return HttpResponse(result)


@post_request
def avg_ticket_close_time(request):
    avg = insights.avg_ticket_close_time()
    response = "0" if not avg else "{0:.2f}".format(avg*24)
    result = json.dumps({"result": response + " "})
    return HttpResponse(result)
