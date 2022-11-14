from django.urls import path
from register.views import index, export_candidates
# from register.sheets import export_to_google


urlpatterns = [
    path('api/', index, name='handler'),
    path("excel/", export_candidates, name="export-candidates"),
    # path("sheets/", export_to_google, name="export-to-google")
]
