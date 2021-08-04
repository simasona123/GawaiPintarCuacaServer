from django.contrib import admin
from .models import UserAndroid, DataMatang, DataMentah

# Register your models here.

# register biasa
# admin.site.register(UserAndroid)
# admin.site.register(DataMentah)
# admin.site.register(DataMatang)

# Register dengan decorator


@admin.register(UserAndroid)
class UserAndroidAdmin (admin.ModelAdmin):
    list_display = ('id', 'uuid', 'model', 'api_version')
    # menampilkan kolom pada admin sesuai dengan kolom pada model


@admin.register(DataMentah)
class DataMentahAdmin (admin.ModelAdmin):
    list_display = ('id', 'user_android', 'timestamp')
    list_filter = ('user_android',)
    # Filter sesuai kolom

@admin.register(DataMatang)
class DataMatangAdmin (admin.ModelAdmin):
    list_display = ('pk', 'suhu_udara', 'kelembaban_udara', 'tekanan_udara' )
