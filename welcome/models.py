from django.db import models


class Account(models.Model):

    class Meta:
        db_table = "accounts"

    user = models.CharField(max_length=100)
    type = models.CharField(max_length=50)


class Ticket(models.Model):

    class Meta:
        db_table = "tickets"

    name = models.CharField(max_length=250)
    updated = models.DateField()


class Message(models.Model):

    class Meta:
        db_table = "messages"

    message = models.TextField(max_length=4000)
    updated = models.DateField()
    fk_ticket = models.ForeignKey(Ticket, db_column="fk_ticket")
    fk_account = models.ForeignKey(Account, db_column="fk_account")
