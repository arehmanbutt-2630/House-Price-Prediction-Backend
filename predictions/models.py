from django.db import models
from django.core.validators import MinValueValidator

class Prediction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    square_footage = models.IntegerField(validators=[MinValueValidator(0)])
    bedrooms = models.IntegerField(validators=[MinValueValidator(1)])
    predicted_price = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['-created_at']
