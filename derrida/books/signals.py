from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AssociatedBook


@receiver(post_save, sender=AssociatedBook)
def build_symmetrical(sender, instance, *args, **kwargs):
    symmetrical_instance = AssociatedBook.objects.get_or_create(
        from_book=instance.to_book,
        to_book=instance.from_book,
        is_collection=instance.is_collection
    )
    if not symmetrical_instance:
        raise Exception('Failed to created a reciprocal relationship')


@receiver(post_delete, sender=AssociatedBook)
def delete_symmetrical(sender, instance, *args, **kwargs):
    try:
        symmetrical_instance = AssociatedBook.objects.get(
            from_book=instance.to_book,
            to_book=instance.from_book,
        )
        symmetrical_instance.delete()
    except ObjectDoesNotExist:
        pass
