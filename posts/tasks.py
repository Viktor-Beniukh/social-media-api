from celery import shared_task

from posts.models import Post


@shared_task
def create_post(data):
    post = Post.objects.create(**data)
    post.save()
