from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    """
    Helps Django work with our custom user model.
    """
    def create_user(self, email, name, password=None):
        """
        creates a new userprofile object.
        """
        if not email:
            raise ValueError('User must have an email.')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates a new superuser profile.
        """
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Represents a user profile inside our system.
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """
        Used to get a users full name.
        """
        return self.name

    def get_short_name(self):
        """
        Used to get a users short name.
        """
        return self.name

    def __str__(self):
        return self.name


class ProfileFeedItem(models.Model):
    """
    Profile status update.
    """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='feeds')
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status_text