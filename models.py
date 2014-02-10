#coding: utf-8
from __future__ import unicode_literals

from django.db import models

from settings import RUSPOST_MANAGERS


class RuspostPerson(models.Model):
    name = models.CharField('имя', max_length=64)
    address = models.CharField('адрес', max_length=255)
    index = models.CharField('индекс', max_length=6)


class RuspostManager(RuspostPerson):
    document = models.CharField('документ', max_length=16, blank=True)
    serie = models.CharField('серия документа', max_length=8, blank=True)
    number = models.CharField('номер документа', max_length=8, blank=True)
    issue_day_month = models.CharField('день и месяц документа', max_length=5, blank=True)
    issue_year = models.CharField('год документа', max_length=2, blank=True)
    issuer = models.CharField('кем выдан документ', max_length=128, blank=True)
    inn = models.CharField('ИНН', max_length=12, blank=True)
    ks = models.CharField('к/с', max_length=20, blank=True)
    bank = models.CharField('банк', max_length=128, blank=True)
    rs = models.CharField('р/с', max_length=20, blank=True)
    bik = models.CharField('бик', max_length=9, blank=True)


class RuspostClient(RuspostPerson):
    pass


class RuspostPrice(models.Model):
    value = models.PositiveIntegerField('ценность', blank=True)
    on_delivery = models.PositiveIntegerField('наложенный платёж', blank=True)


class RuspostOptions(models.Model):
    standard = models.BooleanField('стандартная', default=False)
    heavy = models.BooleanField('тяжёлая', default=False)
    non_standard = models.BooleanField('нестандартная', default=False)
    heavy_big = models.BooleanField('тяжёлая крупногабаритная', default=False)
    usual = models.BooleanField('обычная', default=False)
    valuable = models.BooleanField('с объявленной ценностью', default=True)
    cash_on_delivery = models.BooleanField('с наложенным платежом', default=True)
    with_notification = models.BooleanField('с уведомлением', default=False)
    with_inventory = models.BooleanField('с описью', default=False)
