from celery import shared_task
from .views import perform_draw

@shared_task
def weekly_draw():
    perform_draw()
