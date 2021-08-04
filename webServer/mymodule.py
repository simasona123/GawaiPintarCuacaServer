from time import time
from datetime import datetime, timedelta
from pytz import timezone
from apiServer.models import DataMentah


def last_chart_x_axis():
    now = datetime.now()
    tz = timezone('Asia/Jakarta')
    now = now.astimezone(tz)
    date_format = "%Y-%m-%dT%H:%M:%S%z"
    x_axis = []
    selisih_waktu = timedelta(days=3)
    for i in range(8, -1, -1):
        a = now - i*selisih_waktu
        x_axis.append(a.strftime(date_format))
    return x_axis


def last_chart_y_axis(x_axis):
    y = []
    for i in x_axis:
        a = DataMentah.objects.filter(timestamp__lte=i).count()
        y.append(a)
    return y


def write_data(writer, query_dict):
    writer.writerow(['ts', 'lat', 'long', 'alt', 'alt1', 't', 'tbat',
                     'rh', 'pres', 'tcpu', 'disp', 'charg', 't1', 'rh1', 'p1'])
    for i in query_dict:
        data_matang = i.get_DataMatang()
        if data_matang != None:
            writer.writerow([i.timestamp, i.latitude, i.longitude, i.altitude, i.altitude1, i.suhu_udara, i.suhu_baterai,
                             i.kelembaban_udara, i.tekanan_udara, i.suhu_cpu, i.status_layar, i.status_charging, data_matang.suhu_udara,
                             data_matang.kelembaban_udara, data_matang.tekanan_udara])
        else:
            writer.writerow([i.timestamp, i.latitude, i.longitude, i.altitude, i.altitude1, i.suhu_udara, i.suhu_baterai,
                             i.kelembaban_udara, i.tekanan_udara, i.suhu_cpu, i.status_layar, i.status_charging])

def write_data1(writer, query_dict):
    writer.writerow(['uuid', 'ts', 'lat', 'long', 'alt', 'alt1', 't', 'tbat',
                     'rh', 'pres', 'tcpu', 'disp', 'charg', 't1', 'rh1', 'p1'])
    for i in query_dict:
        data_matang = i.get_DataMatang()
        if data_matang != None:
            writer.writerow([i.user_android, i.timestamp, i.latitude, i.longitude, i.altitude, i.altitude1, i.suhu_udara, i.suhu_baterai,
                             i.kelembaban_udara, i.tekanan_udara, i.suhu_cpu, i.status_layar, i.status_charging, data_matang.suhu_udara,
                             data_matang.kelembaban_udara, data_matang.tekanan_udara])
        else:
            writer.writerow([i.user_android, i.timestamp, i.latitude, i.longitude, i.altitude, i.altitude1, i.suhu_udara, i.suhu_baterai,
                             i.kelembaban_udara, i.tekanan_udara, i.suhu_cpu, i.status_layar, i.status_charging])
