from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('user', 'Пользователь'),
    )
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='user',
        verbose_name='Роль'
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def is_admin(self):
        return self.role == 'admin'