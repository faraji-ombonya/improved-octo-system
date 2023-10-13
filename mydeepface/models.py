from django.db import models
import uuid

class Enroll(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_id = models.UUIDField()
    image = models.ImageField(upload_to="mydeepface/uploads/")

class Recognize(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    image = models.ImageField(upload_to="mydeepface/uploads/")