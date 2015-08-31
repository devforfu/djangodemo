from operator import itemgetter
from datetime import timedelta
from collections import defaultdict

import pandas as pd
from pandas.stats.moments import rolling_mean
from welcome.models import Ticket, Account, Message


__all__ = ['open_tickets_count', 'avg_reply_time', 'avg_ticket_close_time',
           'open_tickets_chart', 'reply_moving_average']


def to_data_frame(cls):
    return pd.DataFrame.from_records(cls.objects.all().values())


def join_tables():
    tickets, messages, accounts = [to_data_frame(c)
                                   for c in (Ticket, Message, Account)]

    m1 = pd.merge(tickets, messages, left_on='id', right_on='fk_ticket_id',
                  suffixes=('_ticket', '_message'))

    m2 = pd.merge(m1, accounts, left_on='fk_account_id', right_on='id',
                  suffixes=('_message', '_account'))

    return m2


def open_tickets_count():
    """
    "How many open tickets exist currently?" - A ticket considered as open
    if the last reply isn't from an expert.
    """

    insight_table = join_tables()

    open_tickets = 0

    for _, group in insight_table.groupby('name'):
        user_type = group.sort('updated_message').iloc[-1].type
        open_tickets += 1 if user_type == 'user' else 0

    return open_tickets


def avg_reply_time():
    """
    "What is the average time until the expert replies" - Ticket is open until
    first reply from expert.
    """
    insight_table = join_tables()

    days_for_waiting = []

    for _, group in insight_table.groupby('name'):
        ticket_update = group.updated_ticket.iloc[0]
        experts_only = group[group.type == 'expert']

        if experts_only.empty:
            continue

        first_reply = experts_only.updated_message.min()

        reply_time = first_reply - ticket_update
        days_for_waiting.append(reply_time.days)

    if not days_for_waiting:
        return None

    avg = sum(days_for_waiting)/len(days_for_waiting)

    return avg


def avg_ticket_close_time():
    """
    "What is the average time until the a ticket is closed" - Ticket open until
    last reply from doctor (expert).
    """
    insight_table = join_tables()

    days_until_closed = []

    for _, group in insight_table.groupby('name'):
        ticket_update = group.updated_ticket.iloc[0]
        group = group.sort('updated_message')
        last_message_user_type = group.iloc[-1].type
        last_message_date = group.iloc[-1].updated_message

        if last_message_user_type == 'expert':
            closing_time = last_message_date - ticket_update
            days_until_closed.append(closing_time.days)

    if not days_until_closed:
        return None

    avg = sum(days_until_closed)/len(days_until_closed)

    return avg


def open_tickets_chart(start_date, end_date):
    """
    Chart (open tickets)
    Build a bar chart that show over time how many open tickets exist
    """
    messages, accounts = to_data_frame(Message), to_data_frame(Account)
    join = pd.merge(messages, accounts,
                    left_on='fk_account_id', right_on='id',
                    suffixes=('_message', '_account')).sort('updated')

    ticket_is_opened = defaultdict(lambda: False)
    result = {}

    # first bar needs look into all previous history
    before_start_date = join.updated <= start_date

    for i, g in join[before_start_date].groupby('fk_ticket_id'):
        is_opened = g.iloc[-1].type == 'user'
        ticket_is_opened[i] = is_opened

    df = join[(join.updated > start_date) & (join.updated <= end_date)]

    next_day = start_date + timedelta(days=1)

    for ts in pd.date_range(next_day, end_date, freq='D'):
        new_messages = df[df.updated == ts.date()]

        if new_messages.empty:
            result[ts.date()] = None
            continue

        new_messages = new_messages.sort('updated')

        for i, g in new_messages.groupby('fk_ticket_id'):
            is_opened = g.iloc[-1].type == 'user'
            ticket_is_opened[i] = is_opened

        opened_tickets_on_current_date = \
            sum(int(v) for v in ticket_is_opened.values())

        result[ts.date()] = opened_tickets_on_current_date

    # convert to dataframe to fill NaN values
    items = sorted(result.items(), key=itemgetter(0))
    result = pd.DataFrame({
        'date': [d for d, _ in items],
        'count': [c for _, c in items]
    })

    result = result.fillna(method='ffill').dropna().to_dict(orient='list')

    return result


def reply_moving_average(start_date, end_date):
    """
    Chart (average reply time with moving average over the last 5 days)
    When you don't know it google what moving average is
    """
    insight_table = join_tables()

    df = insight_table[(insight_table.updated_message >= start_date) &
                       (insight_table.updated_message <= end_date)]

    reply_times = {'date': [], 'avg': []}

    for ts in pd.date_range(start_date, end_date, freq='D'):
        reply_times['date'].append(ts.date())

        expert_answers = \
            df[(df.updated_message <= ts.date()) & (df.type == 'expert')]

        if expert_answers.empty:
            reply_times['avg'].append(None)

        else:
            avgs = expert_answers.groupby('name').apply(
                lambda g: (g.updated_message.min() - g.updated_ticket.iloc[0]))
            avgs = [a.days for a in avgs]
            reply_times['avg'].append(sum(avgs)/len(avgs))


    result = pd.DataFrame.from_dict(reply_times)
    result = result.fillna(method='ffill')
    result = result.dropna()

    result.avg = rolling_mean(result.avg, 5)

    return result.dropna()