from django.db import models
from django.contrib.auth.models import AbstractUser,User
from .managers import CustomUserManager
from django.core.validators import RegexValidator
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from shop.models import Cart



class CustomUser(AbstractUser):
    username = None
    phone_no=models.CharField(max_length=11,unique=True,validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,11}$',
                message="Phone number must be in the format: '0999999999'. Up to 11 digits allowed."
            ),
        ])
    avatar=models.ImageField(default='avatar.png')
    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_no)


@receiver(post_save,sender=CustomUser)
def creatCart(sender, instance, created, **kwargs):
    if created:
        cart=Cart(user=instance)
        cart.save()



