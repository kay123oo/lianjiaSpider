from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view()),
    path('zufang/list/',views.listing),
    path('zufang/a/?district=<district>',views.group_by_district, name= 'group_by_district'),
    path('zufang/a/?bizcircle=<bizcircle>',views.group_by_district, name= 'group_by_bizcircle')
]