from django.urls import path
from .views import screenshot_list, capture_screenshot

urlpatterns = [
    path('screenshot-list/', screenshot_list, name='screenshot_list'),
    path('capture-screenshot/', capture_screenshot, name='capture_screenshot'),
]
