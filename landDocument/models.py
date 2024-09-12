from django.db import models
from datetime import datetime

# Create your models here.
class LandDocument(models.Model):
    document_id = models.AutoField(primary_key=True)
    parcel_Number = models.CharField(max_length=50,default="")
    national_id = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    owner_name = models.CharField(max_length=20)
    address = models.CharField(max_length=30)
    date_sold = models.DateField(max_length=15)
  

   

    objects = models.Manager()

    def __str__(self):
        return f"{self.owner_name} {self.address} "
