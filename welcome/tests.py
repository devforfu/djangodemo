from datetime import date, timedelta
from unittest import skip

from django.test import TestCase
from django.test.client import Client

import welcome.insights as insights


class TestAjaxRequests(TestCase):

    fixtures = ['welcome.json']

    def setUp(self):
        self.client = Client()

    def test_ajax_requests(self):
        data = {'start_date': '8/4/2015', 'end_date': '10/20/2015'}

        # r = self.client.post('/welcome/chart/bar_chart', data=data)
        # self.assertTrue(r.content.decode().startswith('bar chart'))

        r = self.client.post('/welcome/chart/users', data=data)
        # self.assertTrue(r.content.decode().startswith('users'))

    @skip
    def test_data_insights(self):
        start_date = date(month=8, day=9, year=2015)
        end_date = date(month=10, day=8, year=2015)
        result = insights.open_tickets_chart(start_date, end_date)

        result = insights.reply_moving_average(start_date, end_date)

        count = insights.open_tickets_count()
        self.assertTrue(count > 0)

        avg_reply_time = insights.avg_reply_time()
        self.assertTrue(isinstance(avg_reply_time, float))
        self.assertTrue(avg_reply_time > 0)

        avg_close_time = insights.avg_ticket_close_time()
        self.assertTrue(avg_close_time > 0)
