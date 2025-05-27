from django.db import models
from resources.common_functions.custom_id_generator import id_generator


class ReceiptFile(models.Model):
    receipt_file_id = models.CharField(max_length=255, primary_key=True)
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='receipts/')
    is_valid = models.BooleanField(default=False)
    invalid_reason = models.TextField(blank=True, null=True)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'receipt_file'
        managed = True

    def save(self, *args, **kwargs):
        if not self.receipt_file_id:
            self.receipt_file_id = id_generator("REF")
        super().save(*args, **kwargs)


class Receipt(models.Model):
    receipt_id = models.CharField(max_length=255, primary_key=True)
    purchased_at = models.DateTimeField(null=True, blank=True)
    merchant_name = models.CharField(max_length=255, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    file_path = models.ForeignKey(ReceiptFile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'receipt'
        managed = True

    def save(self, *args, **kwargs):
        if not self.receipt_id:
            self.receipt_id = id_generator("RCP")
        super().save(*args, **kwargs)
