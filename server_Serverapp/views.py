from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Screenshot
from celery import shared_task
import requests

def screenshot_list(request):
    screenshots = Screenshot.objects.all()
    screenshot_data = [{'id': screenshot.id, 'image_url': screenshot.image.url} for screenshot in screenshots]
    return JsonResponse({'screenshots': screenshot_data})


@csrf_exempt
def capture_screenshot(request):
    if request.method == 'POST' and request.FILES.get('image'):
        screenshot = request.FILES['image']
        Screenshot.objects.create(image=screenshot)
                
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

# Celery task for capturing and sending screenshots 
@shared_task
def capture_and_send_screenshot_async():
    print("Task started")
    screenshots = Screenshot.objects.all()
    latest_screenshot = screenshots.last()

    if latest_screenshot:
        with open(latest_screenshot.image.path, 'rb') as file:
            files = {'image': file}
            django_server_url = 'http://127.0.0.1:8000/capture-screenshot/'
            response = requests.post(django_server_url, files=files)

        print(response.text)

