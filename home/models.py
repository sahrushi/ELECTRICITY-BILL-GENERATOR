from django.db import models
from django.core.validators import MaxValueValidator
# Create your models here.


class BillDetail(models.Model):
    Name=               models.CharField(max_length=150, default=None)
    CID=                models.IntegerField(unique=True)
    Units=              models.PositiveIntegerField(validators=[MaxValueValidator(1000)], default=None)
    Amount=             models.PositiveIntegerField(validators=[MaxValueValidator(1000)], default=None)
    BillGenerated=      models.DateField(auto_now_add=True)
    def __str__(self):
        return self.Name