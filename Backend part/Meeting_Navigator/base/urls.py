from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('new_meeting/', views.new_meeting, name='new_meeting'),
    path('record_voice/', views.record_voice, name='record_voice'),
    path('show_data/',views.show_data,name='show_data'),
    path('show_summary/<str:meeting_name>/',views.show_summary,name='show_summary'),
]
