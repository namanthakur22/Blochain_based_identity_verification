from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('create', views.create, name="create"),
    path('validate', views.validate, name="validate"),
    path('add_certificate/', views.add_certificate, name='add_certificate'),
    path('verify_certificate/', views.verify_certificate, name='verify_certificate'),
    path('trust_score/', views.trust_score, name='trust_score'),
    path('data_extract/', views.data_extract, name='data_extract'),
]