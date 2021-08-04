from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
import time
import decimal
from .models import DataMentah, DataMatang

logger = get_task_logger(__name__)


def calculate_data(item):
    suhu_udara = item.suhu_udara + item.suhu_baterai * decimal.Decimal(10/100)
    kelembaban_udara = item.kelembaban_udara + \
        item.suhu_udara + item.suhu_baterai * decimal.Decimal(10/100)
    tekanan_udara = item.tekanan_udara + \
        item.suhu_baterai * decimal.Decimal(10/100)
    a = DataMatang(tekanan_udara=tekanan_udara,
                   kelembaban_udara=kelembaban_udara, suhu_udara=suhu_udara)
    a.data_mentah = item
    a.save()


@shared_task(name='process_data_task')
def process_data_task():
    logger.info("Data Sedang Diproses")
    start_time = time.time()
    query = DataMentah.objects.all()
    i = 0
    for item in query:
        if i == 250 or i == 10:
            break
        if item.get_DataMatang() == None:
            calculate_data(item)
            i += 1

    msg = "Data Proses Selesai \n"
    msg = "Waktu yang dibutuhkan " + str(time.time()-start_time)
    logger.info(msg)
    return msg


