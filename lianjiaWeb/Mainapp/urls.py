from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view()),
    path('<city>/list/',views.listing),
    path('gz/list/?district=<district>',views.group_by_district, name= 'group_by_district'),
    path('gz/list/?bizcircle=<bizcircle>',views.group_by_district, name= 'group_by_bizcircle')
]