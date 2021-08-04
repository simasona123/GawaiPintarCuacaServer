from django.urls import path
from .views import Index, ProsesTekanan, User, UserDetail, Data, SendData, LatestData, ProsesRH1, ProsesRH0, ProsesBaterai

urlpatterns = [
    path("", Index.as_view(), name='index'),
    path("user", User.as_view(), name='user'),
    path("user/<int:pk>", UserDetail.as_view(), name='user_detail'),
    path("data", Data.as_view(), name='data'),
    path("send_data", SendData.as_view(), name='send_data'),
    path("latest_data", LatestData.as_view(), name='latest_data'),
    path("proses_rh0", ProsesRH0.as_view(), name='proses_rh0'),
    path("proses_rh1", ProsesRH1.as_view(), name='proses_rh1'),
    path("proses_p0", ProsesTekanan.as_view(), name='proses_tekanan'),
    path("proses_baterai", ProsesBaterai.as_view(), name='proses_baterai'),
]
