from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('relationships_terms', views.relationships_terms, name='scheme'),
    path('createTherm', views.createTherm, name='therm'),
    path('createConnection', views.createConnection, name='connection'),
    path('addXML', views.addXML, name='addXML'),
    path('<str:pk>', views.NewsListView.as_view(), name='news-list'),
    path('<int:pk>/update', views.NewsUpdateView.as_view(), name='news-update'),
]
