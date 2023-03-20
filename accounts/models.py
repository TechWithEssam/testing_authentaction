from django.db import models
from django.conf import settings
from django.utils.text import slugify
import random
import string
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)



User_Model = settings.AUTH_USER_MODEL
Gender_Choices = (
    ("Male", "Male"),
    ("Female", "Female")
)


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_verified = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email               = models.EmailField(verbose_name='email address'.title(),max_length=255,unique=True)
    username            = models.CharField(max_length=250, unique=True, verbose_name="username".title())
    full_name           = models.CharField(max_length=350, verbose_name="your full name".title(), blank=True)
    date_of_birth       = models.DateField(blank=True, null=True,)
    avatar              = models.ImageField(default="avatars/images.jpeg", upload_to="avatars")
    bio                 = models.CharField(max_length=500, blank=True)
    gender              = models.CharField(choices=Gender_Choices, blank=True, max_length=12)
    country             = models.CharField(blank=True, null=True, max_length=200)
    phone_number        = models.CharField(max_length=30, blank=True)
    is_active           = models.BooleanField(default=True)
    is_admin            = models.BooleanField(default=False)
    followers           = models.ManyToManyField(User_Model, blank=True)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
    objects             = UserManager()
    website             = models.URLField(blank=True, null=True, max_length=200)
    facebook_profile    = models.URLField(blank=True, null=True, max_length=200)
    is_verified         = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs) :
        if not self.username :
            new = self.email[:self.email.index("@")]
            add_username = slugify(new + str(random.randint(1000,1000000)))
            self.username = add_username
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
    



class VerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) :
        return self.token
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
        return super().save(*args, **kwargs)
