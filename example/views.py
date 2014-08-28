# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from futupayments.forms import PaymentForm


def home(request):
    order_id = request.GET.get('order_id')

    if order_id:
       payment_form = PaymentForm.create(
           request,
           amount=100,
           order_id=order_id,
           description='Заказ №{0}'.format(order_id),
           client_email='test@test.ru',
           client_phone='+7 912 9876543',
           client_name='Иоганн Кристоф Бах',
           meta='Some meta info',
       )
    else:
       payment_form = None

    return render(request, 'home.html', {
       'payment_form': payment_form,
    })
