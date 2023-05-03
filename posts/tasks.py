from celery import shared_task

from posts.models import Post


@shared_task
def create_post(author_id, content, created_at, post_image, hashtags=None):
    Post.objects.create(
        author_id=author_id,
        content=content,
        created_at=created_at,
        post_image=post_image,
    )

    if hashtags is not None:
        post = Post.objects.latest("created_at")
        post.hashtags.set(hashtags)
