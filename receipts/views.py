from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from receipts.models import ReceiptFile
from receipts.serializer import (
    ReceiptFileSerializer,
    UploadReceiptFileRequestSerializer,
    ValidateReceiptRequestSerializer, ReceiptSerializer
)
from resources.common_functions.response_builder import build_response
from resources import constant
from receipts.service import (
    receipt_file_service,
    receipt_service
)


class UploadReceiptView(generics.CreateAPIView):
    queryset = ReceiptFile.objects.all()
    serializer_class = UploadReceiptFileRequestSerializer

    def create(self, request, *args, **kwargs):
        try:

            upload_files = []
            upload_files_ids = []
            files = request.FILES.getlist('file')
            upload_serializer = self.get_serializer(data=request.data)
            upload_serializer.is_valid(raise_exception=True)
            for file in files:
                _response = receipt_file_service.handle_upload(file)

                # PREPARE RESPONSE DATA
                upload_files.append(_response)
                upload_files_ids.append(_response["receipt_file_id"])

            return build_response(
                data={
                    "data": upload_files,
                    "ids": upload_files_ids
                },
                message="Receipt uploaded successfully.",
                status_code=status.HTTP_201_CREATED,
                response_type=constant.SUCCESS
            )

        except ValidationError as ve:
            return build_response(
                data={},
                message=str(ve.detail),
                status_code=status.HTTP_400_BAD_REQUEST,
                response_type=constant.ERROR
            )

        except Exception as e:
            return build_response(
                data={},
                message=f"An unexpected error occurred: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                response_type=constant.ERROR
            )


class ValidateReceiptView(APIView):
    def post(self, request):
        try:
            serializer = ValidateReceiptRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return build_response(
                    data=[],
                    message=str(serializer.errors),
                    status_code=status.HTTP_404_NOT_FOUND,
                    response_type=constant.FAIL
                )

            _response = receipt_file_service.validate_receipt(request.data)
            return build_response(
                data=_response,
                message="Receipts validated successfully.",
                status_code=status.HTTP_200_OK,
                response_type=constant.SUCCESS
            )

        except Exception as e:
            return build_response(
                data=[],
                message=f"An unexpected error occurred: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                response_type=constant.ERROR
            )


class ProcessReceiptView(APIView):
    def post(self, request):
        try:
            serializer = ValidateReceiptRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return build_response(
                    data=[],
                    message=str(serializer.errors),
                    status_code=status.HTTP_404_NOT_FOUND,
                    response_type=constant.FAIL
                )

            found_pdfs = ReceiptFile.objects.filter(
                receipt_file_id__in=request.data.get("receipt_file_ids", [])
            )
            for _pdf in found_pdfs:
                _response = receipt_file_service.process_receipt(_pdf)
            return build_response(
                data=[],
                message="All Receipts Processed",
                status_code=status.HTTP_200_OK,
                response_type=constant.SUCCESS
            )
        except Exception as e:
            return build_response(
                data=[],
                message=f"An unexpected error occurred: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                response_type=constant.ERROR
            )


class UnProcessReceiptListView(APIView):
    def get(self, request):
        try:
            found_data = receipt_file_service.fetch_all_un_process_receipt()
            serializer = ReceiptFileSerializer(found_data, many=True)
            return build_response(
                data=serializer.data,
                message="Fetch Un-Process Receipt successfully.",
                status_code=status.HTTP_200_OK,
                response_type=constant.SUCCESS
            )

        except Exception as e:
            return build_response(
                data=[],
                message=f"An unexpected error occurred: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                response_type=constant.ERROR
            )


class ProcessReceiptListView(APIView):
    def get(self, request, receipt_id=None):
        try:
            filter_para = None
            # CHECK QUERY PARAMS AVAILABLE NOR NOT FOR FILTER
            if request.query_params:
                filter_para = request.query_params
            if receipt_id is not None:
                receipt = receipt_service.fetch_process_receipt_by_id(receipt_id, filter_para)
                serializer = ReceiptSerializer(receipt)
                return build_response(
                    data=serializer.data,
                    message="Receipt fetched successfully.",
                    status_code=status.HTTP_200_OK,
                    response_type=constant.SUCCESS
                )
            else:
                receipts = receipt_service.fetch_all_process_receipts(filter_para)
                serializer = ReceiptSerializer(receipts, many=True)
                return build_response(
                    data=serializer.data,
                    message="All Receipt Fetch successfully.",
                    status_code=status.HTTP_200_OK,
                    response_type=constant.SUCCESS
                )

        except Exception as e:
            return build_response(
                data=[],
                message=f"An unexpected error occurred: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                response_type=constant.ERROR
            )
