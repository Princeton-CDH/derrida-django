from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import AssociatedBook


@receiver(post_save, sender=AssociatedBook)
def build_symmetrical(sender, instance, *args, **kwargs):
        print('Build event fired!')
        symmetrical_instance = AssociatedBook.objects.get_or_create(
            from_book=instance.to_book,
            to_book=instance.from_book,
        )
        if not symmetrical_instance:
            raise Exception


@receiver(pre_delete, sender=AssociatedBook)
def delete_symmetrical(sender, instance, *args, **kwargs):
        print('Delete event fired!')
        try:
            symmetrical_instance = AssociatedBook.objects.get(
                from_book=instance.to_book,
                to_book=instance.from_book,
            )
            symmetrical_instance.delete()
        except ObjectDoesNotExist:
            pass
