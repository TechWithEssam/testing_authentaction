from django.db.models.signals import post_save
from .models import User, VerificationToken




def create_verification_token(sender, instance, created, **kwargs):
    if created:
        VerificationToken.objects.create(user=instance)
post_save.connect(create_verification_token, sender=User)