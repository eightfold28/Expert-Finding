from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('searchresult/', views.searchresult, name='searchresult'),
	path('expertprofile/<int:pk>/', views.expertprofile, name='expertprofile'),
	path('about/', views.about, name = 'about'),
]