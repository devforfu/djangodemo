from unittest import skip
from datetime import date, timedelta

import pandas as pd
from django.test import TestCase
from django.test.client import Client

import welcome.insights as insights


class TestAjaxRequests(TestCase):

    fixtures = ['welcome.json']

    def setUp(self):
        self.client = Client()

    @skip
    def test_ajax_requests(self):
        data = {'start_date': '05/01/2015', 'end_date': '08/07/2015'}

        self.client.post('/welcome/chart/open_tickets')
        self.client.post('/welcome/chart/avg_reply_time')
        self.client.post('/welcome/chart/avg_ticket_close_time')

        r = self.client.post('/welcome/chart/bar_chart', data=data)
        r = self.client.post('/welcome/chart/users', data=data)

    @skip
    def test_numeric_data_insights(self):
        count = insights.open_tickets_count()
        self.assertTrue(count > 0)

        avg_reply_time = insights.avg_reply_time()
        self.assertTrue(isinstance(avg_reply_time, float))
        self.assertTrue(avg_reply_time > 0)

        avg_close_time = insights.avg_ticket_close_time()
        self.assertTrue(avg_close_time > 0)

    def test_filter_data_insights(self):
        start_date = date(month=8, day=25, year=2015)
        end_date = date(month=9, day=15, year=2015)

        # insights.open_tickets_chart(start_date, end_date)

        insights.reply_moving_average(start_date, end_date)
