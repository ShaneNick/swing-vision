from django.urls import path
from .views import outcomes_page  

urlpatterns = [
    path('outcomes/', outcomes_page, name='outcomes'),  
]
