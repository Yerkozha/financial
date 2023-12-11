from celery import shared_task

@shared_task
def update_news(flags):
    '''
        PERFORM UPDATE NEWS 00:00
    '''

    return [flags]