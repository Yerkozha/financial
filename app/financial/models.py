# Create your models here.

from django.db import models


class Financial(models.Model):

    predsedatelSovetaDirektorov = models.CharField(max_length=255, null=True, blank=True)
    predsedatel_pravleniya = models.CharField(max_length=100, null=True, blank=True)
    sovet_direktorov = models.CharField(max_length=100, null=True, blank=True)
    chleny_pravleniya = models.CharField(max_length=100, null=True, blank=True)
    glavnyy_buhgalter = models.CharField(max_length=100, null=True, blank=True)
    bin = models.CharField(max_length=20, null=True)
    address = models.TextField(null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    fax = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    bank_vtorogo_urovnya = models.JSONField(default=list, null=True, blank=True)
    kastodian = models.JSONField(default=list, null=True, blank=True)
    bankovskie_holdingi = models.JSONField(default=list, null=True, blank=True)

    def __str__(self):
        return f"{self.bin} - {self.predsedatelSovetaDirektorov}"


