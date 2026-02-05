from django.db import models

class UploadBatch(models.Model):
    """
    Tracks the uploaded file and when it happened.
    This helps us implement 'History Management' later.
    """
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upload at {self.uploaded_at}"

class ChemicalEquipment(models.Model):
    """
    Stores the actual parsed data from the CSV.
    Fields match the requirements: Name, Type, Flowrate, Pressure, Temperature.
    """
    # Link this data to a specific upload batch
    batch = models.ForeignKey(UploadBatch, on_delete=models.CASCADE, related_name='equipments')
    
    # Data columns from the CSV
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()

    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"