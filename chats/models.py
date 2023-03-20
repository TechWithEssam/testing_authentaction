from django.db import models
from products.models import Product
from accounts.models import User
from django.utils import timezone
import uuid
from django.urls import reverse
# Create your models here.


class Chat(models.Model) :
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True,null=True, related_name="product")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,null=True)
    default_message = models.CharField(max_length=200, default="is this available")
    slug = models.SlugField(blank=True, null=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f"messege of product {self.product.name}"
    def save(self, *args, **kwargs) :
        if not self.slug :
            self.slug = uuid.uuid4()
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self) :
        return reverse("chats:prived_message", kwargs={"slug":self.slug})
    @property
    def all_messages(self) :
        return self.chat.all()
    @property
    def last_message(self) :
        message = self.all_messages.last()
        return message
    
class Messages(models.Model) :
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f"{str(self.user)}"