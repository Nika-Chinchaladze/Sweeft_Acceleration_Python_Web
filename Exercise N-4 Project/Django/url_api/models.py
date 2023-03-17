from django.db import models

# Create your models here.
class Client(models.Model):
    client_name = models.CharField(max_length=100, unique=True, null=False)
    is_premium_client = models.BooleanField(null=False)

    def __str__(self):
        return f"{self.client_name} {self.is_premium_client}"


class Link(models.Model):
    original_link = models.CharField(max_length=250, null=False)
    shortened_link = models.CharField(max_length=100, unique=True, null=False)
    creation_date = models.CharField(max_length=100, null=False)
    access_counter = models.IntegerField(null=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.original_link} {self.shortened_link} {self.creation_date} {self.access_counter} {self.client}"
    