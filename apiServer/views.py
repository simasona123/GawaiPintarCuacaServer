from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views import View

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.views import APIView

from keras.models import load_model
import pickle

from .models import UserAndroid, DataMentah, DataMatang
from .serializers import DataMentahSerializer,  UserAndroidSerializer, ResponseUser, InputData, LastData, DataMentahSerializer1

import threading
import time
from datetime import timedelta

from modelML.genetic import prediction_rh1
from modelML.p0 import predict_pa
from modelML.rh_perhitungan import cari_rh0_awal, cari_rh1
from modelML.t_baterai import prediction1
from skripsi.mycron import catatan


class ThreadingInputData(threading.Thread):
    def __init__(self, user, data):
        super().__init__()
        self.user = user
        self.data = data

    def run(self):
        try:
            data_diterima=[]
            time.sleep(2)
            data1 = self.data
            data_tersimpan = 0
            for i in range(len(data1)):
                data1[i]['latitude'] = round(data1[i]['latitude'], 4)
                data1[i]['longitude'] = round(data1[i]['longitude'], 4)
                data1[i]['altitude'] = round(data1[i]['altitude'], 3)
                data1[i]['altitude1'] = round(data1[i]['altitude1'], 3)
                data1[i]['suhu_cpu'] = round(data1[i]['suhu_cpu'], 2)
                data1[i]['suhu_baterai'] = round(data1[i]['suhu_baterai'],2)
                data1[i]['tekanan_udara'] = round(data1[i]['tekanan_udara'],2)
                data1[i]['suhu_udara'] = round(data1[i]['suhu_udara'],2)
                data1[i]['kelembaban_udara'] = round(data1[i]['kelembaban_udara'],2)
                serializer = InputData(data=data1[i]) #mengubah ke dalam data yang telah tervalidasi
                if serializer.is_valid():
                    data = serializer.data
                    if float(data['suhu_udara']) < -80 or float(data['suhu_udara']) > 60:
                        print(f"Nilai Suhu Udara Di Luar Batas, Nilai input suhu {data['suhu_udara']}")
                        data['suhu_udara'] = 0
                    if float(data['kelembaban_udara']) < 0 or float(data['kelembaban_udara']) > 100:  # Tambahan RangeCheck
                        print(f"Nilai Kelembaban Udara Di Luar Batas, Nilai input kelembapanS {data['kelembaban_udara']}")
                        data['kelembaban_udara'] = 0
                    if float(data['tekanan_udara']) < 500 or float(data['tekanan_udara']) > 1100:
                        print(f"Nilai Tekanan Udara Di Luar Batas, Nilai input tekanan {data['tekanan_udara']}")
                        data['tekanan_udara'] = 0    
                    a = DataMentah(user_android=self.user, timestamp=data['timestamp'], latitude=data['latitude'],
                               longitude=data['longitude'], altitude=data['altitude'], altitude1=data['altitude1'],
                               suhu_udara=data['suhu_udara'], suhu_baterai=data['suhu_baterai'],
                               kelembaban_udara=data['kelembaban_udara'], tekanan_udara=data['tekanan_udara'],
                               suhu_cpu=data['suhu_cpu'], status_layar=data['status_layar'],
                               status_charging=data['status_charging'])
                    data_diterima.append(a)
                    data_tersimpan += 1
                else:
                    print(serializer.errors)
            DataMentah.objects.bulk_create(data_diterima) # TODO Untuk pengujian server baris ini di-comment
            print(f"Data Tersimpan Sebanyak = {data_tersimpan}")
        except Exception as e:
            print(e)

sentinel = object()
#Lakukan pengolahan berurutan dari RH1, P0, Baterai, dan RH0

#Olah data mentah yang memiliki nilai sensor RH dan Insha Allah Sudah Berhasil
class TProsesRH1(threading.Thread):
    def __init__ (self):
        super().__init__()

    def run(self):
        data_prediksi = []
        try:
            time.sleep(1)
            pk = 0
            total_data = 0
            nama = "Proses RH1"
            model = load_model('prediksi_rh1.h5')
            cache_key = "rh1_"
            if cache.get(cache_key+"pk_terbesar", sentinel) is sentinel:
                pk = 0
                print(f"pk non cache {pk}")
            else :
                pk = cache.get(cache_key+"pk_terbesar")
                print(f"pk cache {pk}")
            a = DataMentah.objects.filter(pk__gt=pk)
            a = a.filter(kelembaban_udara__gt=0, suhu_udara__gt=0)
            i = 0
            for item in a:
                if i == 0 :
                    i += 1
                    pk = item.pk
                if item.get_DataMatang() == None:
                    pred = prediction_rh1(model, item.kelembaban_udara, item.suhu_udara)
                    a = DataMatang(data_mentah=item, kelembaban_udara=pred, suhu_udara=0, tekanan_udara=0)
                    data_prediksi.append(a)
                    total_data += 1
                    print("prediksi ", pred)
            DataMatang.objects.bulk_create(data_prediksi, 200)
            cache.set(cache_key+"pk_terbesar", pk, None) #4 Jam
            catatan(nama, total_data)
        except Exception as e:
            print (e)
                
class TProsesP0(threading.Thread):
    def __init__(self):
        super().__init__()
    
    def run(self):
        try:
            time.sleep(1)
            with open('tekanan.pkl', 'rb') as model:
                regressor = pickle.load(model)
            cache_key = "tekanan_udara"
            data_temp1 = []
            jumlah_data = 0
            nama = "Proses Tekanan Udara"
            if cache.get(cache_key, sentinel) is sentinel :
                datas = DataMentah.objects.filter(tekanan_udara__gt=0)
                print("1 = ", cache.get(cache_key))
            else :
                pk = cache.get(cache_key)
                datas = DataMentah.objects.filter(pk__gt=pk)
                datas = datas.filter(tekanan_udara__gt=0)
                print("2 = ", pk)
            jumlah_datas = datas.count()
            print(jumlah_datas)
            i = 0
            for data in datas :
                data_matang = data.get_DataMatang()
                if data_matang == None:
                    tekanan_udara = predict_pa(regressor, data.tekanan_udara)[0].item()
                    a = DataMatang.objects.create(data_mentah=data, tekanan_udara=tekanan_udara, kelembaban_udara=0, suhu_udara=0)
                    a.save()
                    
                else:
                    tekanan_udara = predict_pa(regressor, data.tekanan_udara)
                    data_matang.tekanan_udara = tekanan_udara[0].item()
                    data_temp1.append(data_matang)
                   
                if  i == 0:
                    cache.set(cache_key, data.id, None) #TODO ubah menjadi 4 Jam Cache Tekanan Udara
                    print("cache terbuat ", {cache.get(cache_key)})
                    i += 1

                jumlah_data += 1

            DataMatang.objects.bulk_update(data_temp1, ['tekanan_udara'], 200)
            catatan(nama, jumlah_data)
        except Exception as e:
            print(e)

#Baterai yang baru
class TProsesBaterai(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        try:
            time.sleep(1)
            model = load_model('Suhu_Baterai_T4.h5')
            users = UserAndroid.objects.all()
            data_matang_total_update = []
            total_data = 0
            cache_key = "baterai_"
            nama = "Proses Suhu Baterai"
            for user in users: #mengambil data pertama setiap user dan dicek untuk dicari hp yang tidak memiliki sensor suhu udara dan kelembaban udara 
                # if (str(user.uuid) != "db76cc1b-6f88-4089-8e50-66bcd0c2561c"):
                #     continue
                data = DataMentah.objects.filter(user_android=user).first() 
                cache_baterai = cache.get(cache_key+str(user.uuid), sentinel)
                print(f"Cache is sentinel {cache_baterai is sentinel}")
                print(user, cache_baterai)
                if data.kelembaban_udara == 0  and data.suhu_udara == 0 and (cache_baterai == sentinel or cache_baterai==0):
                    datas = DataMentah.objects.filter(user_android=user).order_by('timestamp')
                elif data.kelembaban_udara == 0  and data.suhu_udara == 0 and cache_baterai != sentinel:
                    datas = DataMentah.objects.filter(timestamp__gte=cache_baterai, user_android=user).order_by('timestamp')
                else :
                    continue
                i = 0
                jumlah_data = datas.count()
                print(jumlah_data)
                if jumlah_data <=4:
                    cache.set(cache_key+str(user.uuid), datas[0].timestamp, None)
                print(datas)
                #datas adalah DataMentah yang tidak memiliki sensor suhu dan kelembaban
                timestamp_terakhir = None
                selisih = timedelta(minutes=2)
                for item in datas:
                    data_matang = item.get_DataMatang()
                    print("i => ", i)  
                    if cache_baterai == sentinel:
                            layar = [item.status_layar, 0, 0, 0, 0]
                            charging = [item.status_charging, 0, 0, 0, 0]
                            float_suhu_baterai = float(item.suhu_baterai)
                            print("pertama kali ", float_suhu_baterai, item.timestamp, layar, charging)
                            x = prediction1(model, float_suhu_baterai, item.timestamp, layar, charging)
                            # print(type(x), x)
                            if data_matang == None:
                                a = DataMatang(data_mentah=item, suhu_udara=x, kelembaban_udara=0, tekanan_udara=0)
                                a.save()
                                print("Prediksi1 = ", a)
                            else:
                                data_matang.suhu_udara = x
                                data_matang_total_update.append(data_matang)
                                print("Prediksi2 = ", data_matang)
                            cache.set(cache_key+str(user.uuid), 0, None)
                            cache_baterai = cache.get(cache_key+str(user.uuid), sentinel)
                            print("CACHE Terpasang => ", cache_baterai)
                            total_data += 1 

                    elif i > 0 and cache_baterai != sentinel:
                        item_timestamp = item.timestamp
                        if cache_baterai == 0 and i < 5:
                            # print("i lebih kecil dari 5")
                            if i == 1:
                                layar = [item.status_layar, datas[i-1].status_layar, 0, 0, 0]
                                charging =  [item.status_charging, datas[i-1].status_charging, 0, 0, 0]
                            elif i == 2:
                                layar = [item.status_layar, datas[i-1].status_layar, datas[i-2].status_layar, 0, 0]
                                charging =  [item.status_charging, datas[i-1].status_charging, datas[i-2].status_charging, 0, 0]
                            elif i == 3:
                                layar = [item.status_layar, datas[i-1].status_layar, datas[i-2].status_layar, datas[i-3].status_layar, 0]
                                charging =  [item.status_charging, datas[i-1].status_charging, datas[i-2].status_charging, datas[i-3].status_charging, 0]
                            elif i == 4:
                                layar = [item.status_layar, datas[i-1].status_layar, datas[i-2].status_layar, datas[i-3].status_layar, datas[i-4].status_layar]
                                charging =  [item.status_charging, datas[i-1].status_charging, datas[i-2].status_charging, datas[i-3].status_charging, datas[i-4].status_charging]
                        
                        elif i < 4 and data_matang != None:
                            print("lebih kecil 4")
                            i += 1
                            continue

                        else:
                            # print("else")
                            layar = [item.status_layar]
                            charging = [item.status_charging]
                            for j in range (1, 5):
                                item1_timestamp = datas[i-j].timestamp
                                if item_timestamp - item1_timestamp > j*selisih:
                                    layar.append(False)
                                    charging.append(False)
                                else:
                                    # print("Kurang 2 Menit")
                                    layar.append(datas[i-j].status_layar)
                                    charging.append(datas[i-j].status_charging)
                        
                        print("kedua dst ", item.suhu_baterai, item_timestamp, layar, charging)
                        float_suhu_baterai = float(item.suhu_baterai)
                        x = prediction1(model, float_suhu_baterai, item_timestamp, layar, charging)
                        if data_matang == None:
                            a = DataMatang(data_mentah=item, suhu_udara=x, kelembaban_udara=0, tekanan_udara=0)
                            a.save()
                            print("Prediksi3 = ", a)
                        else:
                            data_matang.suhu_udara = x
                            data_matang_total_update.append(data_matang)
                            print("Prediksi4 = ", data_matang)
                        timestamp_terakhir = item.timestamp
                        total_data += 1 

                    if i  == jumlah_data - 4 and timestamp_terakhir != None:
                        cache.set(cache_key+str(user.uuid), timestamp_terakhir, None)   #data.timestamp adalah timestamp dari data pertama hasil query yang #merupakan data paling terbaru
                        print(f"cache => {timestamp_terakhir}") 
                             
                    i += 1  

            DataMatang.objects.bulk_update(data_matang_total_update, ['suhu_udara'], 200)
            catatan(nama, total_data)
        except Exception as e:
            print(e)

# #Olah Data memanfaatkan proses baterai untuk memperoleh nilai kelembabanudara
class TProsesRH0(threading.Thread):
    def __init__ (self):
        super().__init__()

    def run(self):
        try:
            time.sleep(1)
            users = UserAndroid.objects.all()
            data_matang_total = []
            total_data = 0
            nama = "Proses RH0"
            cache_key='rh0_'
            for user in users: #mengambil data pertama setiap user dan dicek untuk dicari hp yang tidak memiliki sensor suhu udara dan kelembaban udara 
                # if (str(user.uuid) != "b51e5bb3-64a1-42a6-982d-42c887c53bfd"):
                #     continue
                data = DataMentah.objects.filter(user_android=user).first() 
                cache_rh0 = cache.get(cache_key+str(user.uuid), sentinel)
                print(user)
                print(f"Cache is sentinel {cache_rh0 is sentinel}")
                print(cache_rh0)
                if data.kelembaban_udara == 0  and data.suhu_udara == 0 and cache_rh0  == sentinel:
                    datas = DataMentah.objects.filter(user_android=user).order_by('timestamp')
                elif data.kelembaban_udara == 0  and data.suhu_udara == 0 and cache_rh0 != sentinel:
                    datas = DataMentah.objects.filter(timestamp__gte=cache_rh0[0], user_android=user).order_by('timestamp')
                    rh0 = cache_rh0[1]
                else :
                    continue
                i = 0
                print(datas)
                jumlah_data = datas.count()
                print(jumlah_data)
                # print(datas)
                #datas adalah DataMentah yang tidak memiliki sensor suhu dan kelembaban
                timestamp_terakhir = None
                for item in datas:
                    data_matang1 = item.get_DataMatang()
                    if data_matang1 != None :
                        # print(data_matang1)
                        if cache_rh0 == sentinel and data_matang1.suhu_udara != 0:
                            x = cari_rh0_awal(item.timestamp, float(data_matang1.suhu_udara))
                            # print(type(x), x)
                            rh0 = x.item()
                            # print(rh0)
                            data_matang1.kelembaban_udara = rh0
                            data_matang_total.append(data_matang1)
                            cache.set(cache_key+str(user.uuid), (item.timestamp, rh0), None)
                            cache_rh0 = cache.get(cache_key+str(user.uuid), sentinel)
                            total_data += 1 

                        elif i > 0 and cache_rh0 != sentinel and data_matang1.suhu_udara != 0:
                            print(item, data_matang1, datas[i-1], datas[i-1].get_DataMatang())
                            data_matang0 = datas[i - 1].get_DataMatang()
                            float_suhu0 = float(data_matang0.suhu_udara)
                            float_suhu1 = float(data_matang1.suhu_udara)
                            x = cari_rh1(item.timestamp, float_suhu1, rh0, float_suhu0)
                            rh0 = x[1]
                            data_matang1.kelembaban_udara = x[0]
                            data_matang_total.append(data_matang1)
                            timestamp_terakhir = item.timestamp
                            total_data += 1 

                        if i  == jumlah_data - 1 and timestamp_terakhir != None :
                            cache.set(cache_key+str(user.uuid), (timestamp_terakhir, rh0), None)   #data.timestamp adalah timestamp dari data pertama hasil query yang #merupakan data paling terbaru
                            print(f"Cache Set => {timestamp_terakhir}")      
                    else:
                        continue
                    i += 1
                # break
            DataMatang.objects.bulk_update(data_matang_total, ['kelembaban_udara'], 200)
            # print(data_matang_total)
            catatan(nama, total_data)
        except Exception as e:
            print (e)


class Index (View):
    template_name = 'apiServer/index.html'
    link = {
        0: "http://gawaipintarcuaca.online/api",
        1: "http://gawaipintarcuaca.online/api/user",
        2: "http://gawaipintarcuaca.online/api/data",
        3: "http://gawaipintarcuaca.online/api/send_data",
        4: "http://gawaipintarcuaca.online/api/latest_data"
    }

    def get(self, request):
        return render(request, template_name=self.template_name, context={'link': self.link})


class User (generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = UserAndroid.objects.all()
    serializer_class = UserAndroidSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        for i in queryset:
            self.perform_destroy(i)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail (generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = UserAndroid.objects.all()
    serializer_class = UserAndroidSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs['pk']
        queryset = get_object_or_404(self.get_queryset(), pk=pk)
        return queryset


class Data (generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = DataMentah.objects.all()
    serializer_class = DataMentahSerializer

    def post(self, request, *args, **kwargs):
        self.serializer_class = DataMentahSerializer1
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.serializer_class = DataMentahSerializer
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SendData (APIView):
    # API untuk mengirim data dari android ke server
    def post(self, request, *args, **kwargs):
        data = request.data
        # Mengecek user apakah sudah ada, jika belum maka data user dibuat
        jumlah_user = UserAndroid.objects.filter(uuid=data['uuid']).count()
        if jumlah_user == 0:
            UserAndroid.objects.create(
                uuid=data['uuid'], model=data['model'], api_version=data['api_version'])
        print(f"Proses penerimaan data dari {data['uuid']}.....")
        user_all = UserAndroid.objects.all()
        user = user_all.filter(uuid=data['uuid']).get()
        user_maks = user_all.last() 
        user_maks = user_maks.id
        user_id = 0
        for item in user_all :
            if item == user:
                break
            user_id += 1
        response_to_sender = {'user_maks': user_maks, 'user': user_id}
        # Mengecek apakah python datatype dapat masuk ke serializer (mengubah python native ke json)
        serializer_data = ResponseUser(data=response_to_sender)

        if serializer_data.is_valid():
            data = data['data']
            t1 = ThreadingInputData(user=user, data=data)
            t1.start()
            return Response(serializer_data.data, 201)
        return Response(status=400)


class LatestData (APIView):
    def get(self, request, *args, **kwargs):
        queryset = UserAndroid.objects.all()
        data = []
        for item in queryset:
            try:
                data.append(item.data_mentah.latest("timestamp"))
            except Exception as e:
                print(e)
        serializer = LastData(data, many=True)
        data = serializer.data
        return Response(serializer.data, 200)


class ProsesRH1 (View):
    template_name = 'apiServer/prosesData.html'
    data = "RH1"
    def get(self, request, *args, **kwargs):
         context = {'data': self.data}
         t1 = TProsesRH1()
         t1.start()  
         return render(request, template_name=self.template_name, context=context)

class ProsesRH0(View):
    template_name = 'apiServer/prosesData.html'
    data = "RH0"
    def get(self, request, *args, **kwargs):
         context = {'data': self.data}
         t1 = TProsesRH0()
         t1.start()
         return render(request, template_name=self.template_name, context=context)

class ProsesTekanan (View):
   template_name = 'apiServer/prosesData.html'
   data = "P0"
   def get(self, request, *args, **kwargs):
       context = {'data' : self.data}
       t1 = TProsesP0()
       t1.start()
       return render (request, template_name=self.template_name, context=context)

class ProsesBaterai(View):
    template_name = 'apiServer/prosesData.html'
    data = "Proses Suhu Baterai"
    def get(self, request, *args, **kwargs):
       context = {'data' : self.data}
       t1 = TProsesBaterai()
       t1.start()
       return render (request, template_name=self.template_name, context=context)

