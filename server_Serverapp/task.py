from celery import shared_task
from .models import Screenshot
import requests
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, backend='django_celery_results.backends.database:DatabaseBackend')
def capture_and_send_screenshot_async(self):
    try:
        logger.info('Task started.')
        
        # To Fetch the latest screenshot
        latest_screenshot = Screenshot.objects.last()

        if latest_screenshot:
            with open(latest_screenshot.image.path, 'rb') as file:
                files = {'image': file}
                django_server_url = 'http://127.0.0.1:8000/capture-screenshot/'
                
                # Use 'self.request.id' to uniquely identify the task instance
                logger.info(f'Task ID: {self.request.id} - Sending screenshot to {django_server_url}')
                
                response = requests.post(django_server_url, files=files)

                logger.info(f'Task ID: {self.request.id} - Task completed: {response.status_code}, {response.text}')
                
                
                return {'status_code': response.status_code, 'content': response.text}
        else:
            logger.error('Task ID: {self.request.id} - No screenshots available.')
            return {'status': 'error', 'message': 'No screenshots available'}

    except Exception as e:
        logger.error(f'Task ID: {self.request.id} - Error during task execution: {str(e)}')
        return {'status': 'error', 'message': str(e)}
