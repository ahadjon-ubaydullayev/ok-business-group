from django.urls import path
from register.views import index, export_candidates


urlpatterns = [
    path('api/', index, name='handler'),
    path("", export_candidates, name="export-candidates")
  
   
]