from django.db import models
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.


class UserAndroid (models.Model):
    uuid = models.UUIDField()
    model = models.CharField(max_length=20)
    api_version = models.CharField(max_length=12)

    def __str__(self):
        return (f"{self.uuid}")

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = 'user_android'
        constraints = [
            models.UniqueConstraint(
                fields=['uuid', 'model'], name="unique_user_android")
        ]


class DataMentah (models.Model):
    user_android = models.ForeignKey(
        UserAndroid, on_delete=models.CASCADE, verbose_name="user_android yang merekam", related_name='data_mentah')
    timestamp = models.DateTimeField()
    longitude = models.DecimalField(max_digits=7, decimal_places=4)
    latitude = models.DecimalField(max_digits=6, decimal_places=4)
    altitude = models.DecimalField(max_digits=7, decimal_places=3)
    altitude1 = models.DecimalField(max_digits=7, decimal_places=3)
    suhu_udara = models.DecimalField(max_digits=4, decimal_places=2)
    suhu_baterai = models.DecimalField(max_digits=4, decimal_places=2)
    kelembaban_udara = models.DecimalField(max_digits=5, decimal_places=2)
    tekanan_udara = models.DecimalField(max_digits=6, decimal_places=2)
    suhu_cpu = models.DecimalField(max_digits=4, decimal_places=2)
    status_layar = models.BooleanField()
    status_charging = models.BooleanField()

    def get_DataMatang(self):
        try:
            return self.data_matang
        except ObjectDoesNotExist:
            return None

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "data mentah"
        constraints = [
            models.UniqueConstraint(
                fields=['user_android', 'timestamp'], name='unique_data_mentah'
            )
        ]


class DataMatang (models.Model):
    # on_delete cascade jika yang ditunjuk yang dihapus maka terhapus dua-duanya
    # jika yang child dihapus maka yang ditunjuk tidak dihapus
    data_mentah = models.OneToOneField(
        DataMentah, on_delete=models.CASCADE, primary_key=True, verbose_name="data_mentah related", related_name='data_matang')
    suhu_udara = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    kelembaban_udara = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    tekanan_udara = models.DecimalField(
        max_digits=6, decimal_places=2, null=True)

    class Meta:
        verbose_name_plural = 'data matang'

    def __str__(self):
        return (f'{self.suhu_udara}C, {self.kelembaban_udara}%, {self.tekanan_udara}mBar')