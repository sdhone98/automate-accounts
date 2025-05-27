from rest_framework import serializers
from receipts.models import (
    ReceiptFile,
    Receipt
)


class ReceiptFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptFile
        fields = '__all__'


class UploadReceiptFileRequestSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    def validate_file(self, value):
        # CHECK FILE EXTENSION
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        return value


class ValidateReceiptRequestSerializer(serializers.Serializer):
    receipt_file_ids = serializers.ListField(
        child=serializers.CharField(), required=True
    )

    def validate_receipt_file_ids(self, value):
        invalid_ids = [
            receipt_id for receipt_id in value
            if not ReceiptFile.objects.filter(receipt_file_id=receipt_id).exists()
        ]
        if invalid_ids:
            raise serializers.ValidationError(
                f"The following receipt file(s) do not exist: {', '.join(invalid_ids)}"
            )
        return value


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'
