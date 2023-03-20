from django.db.models.signals import pre_save, post_save
from .models import Brand, Product, Category
from random import randint
from uuid import uuid4
from django.utils.text import slugify
from django.dispatch import receiver
from .utils import slugify_name_of_product


def pre_save_slugify_category(instance, sender, **kwargs) :
    if not instance.slug :
        random = randint(1000000,10000000)
        instance.slug = slugify(instance.name + str(random))
pre_save.connect(pre_save_slugify_category, sender=Category)

@receiver(post_save, sender=Brand)
def post_save_slugfiy_brand(instance, sender, created, **kwargs) :
    if created :
        if not instance.slug :
            instance.slug = slugify(instance.name + str(uuid4())[:12])
            instance.save()

def post_save_slug_name_product(sender, instance, created, **kwargs) :
    if created :
        if not instance.slug :
            instance.slug = slugify(str(uuid4())[:22])
            instance.save()
post_save.connect(post_save_slug_name_product, sender=Product)