from django.db import models
from django.contrib.auth.models import User
from main.models import AbstractModel


class Profile(AbstractModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(
        default='default_user_image.jpg', upload_to='profile_images')

    def __str__(self):
        return f"{self.user.username}'s Profile"
