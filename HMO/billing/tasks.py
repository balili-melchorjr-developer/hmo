from __future__ import absolute_import, unicode_literals

from celery import shared_task, Celery

from datetime import datetime, timedelta

from billing.models import *

import datetime
import time

@shared_task
def type_hello(*args):
    counter = '00001'
    return counter

@shared_task
def reset_soa_counter(counter):
    print(f'Counter reset to {counter}')