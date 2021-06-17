from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
    if instance._state.adding is True and not instance.is_superuser:
        instance.is_active = False
