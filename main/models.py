from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MainUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a MainUser with the given user_id and password.
        """
        if not username:
            raise ValueError('The username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given user_id and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class MainUser(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=8)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = None
    
    objects = MainUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name_plural = '   Пользователи'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
    
class Lobby_EN(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='messages_en')
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ''

    class Meta:
        verbose_name_plural = '  Лобби EN'

class Lobby_RU(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='messages_ru')
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ''

    class Meta:
        verbose_name_plural = ' Лобби RU'
