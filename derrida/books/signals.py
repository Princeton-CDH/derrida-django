from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AssociatedBook


# NOTES: These signals serve to keep the two relatinoships symmetrical since
# Django does not manage this with a through model to itself, i.e. we want
# both books to be from_book and to_book to one another.

# For the why, see https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.ManyToManyField.through_fields
# and also https://docs.djangoproject.com/en/1.11/topics/db/models/#extra-fields-on-many-to-many-relationships (see restrictions)
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
