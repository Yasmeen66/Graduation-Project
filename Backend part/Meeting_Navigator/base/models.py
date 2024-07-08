from django.db import models
from django.db.models import Model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class RecordEntry(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='record_entries',null=True)
    meeting_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=200, unique=True)
    content = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    # quiz=models.TextField(blank=True, null=True)
    # report = models.TextField(blank=True,null=True)
    # Ques = models.TextField(blank=True,null=True)

    def __str__(self):
        if self.meeting_name:
            return self.meeting_name[:20]
        return "No Meeting Name"
