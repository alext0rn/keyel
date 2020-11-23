from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True, verbose_name ='Дата народження')
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, verbose_name ='Фото')

    def __str__(self):
        return 'Профіль для користувача {}'.format(self.user.username)

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'
