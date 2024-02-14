from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User 
from PIL import Image

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Add or change related_name for groups and user_permissions
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # Choose a suitable related_name
        related_query_name="user",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",  # Choose a suitable related_name
        related_query_name="user",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    def __str__(self):
        return self.username
    
# represents the Profile object
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=200)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to="images/profile/", blank=True)

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
    def __str__(self):
        return self.name

