from django.urls import path
from .views import user_history_rec, nav_history_latest

urlpatterns = [
    path('user_nav_history_latest_products/', nav_history_latest.as_view(), name='nav_history_latest'),
    path('user_history_recommendations/', user_history_rec.as_view(), name='user_history_rec'),
]
