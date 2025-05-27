from django.urls import path
from receipts import views

urlpatterns = [
    path('upload', views.UploadReceiptView.as_view(), name='upload'),
    path('validate', views.ValidateReceiptView.as_view(), name='validate'),
    path('process', views.ProcessReceiptView.as_view(), name='process'),
    path('un-process', views.UnProcessReceiptListView.as_view(), name='un-process'),
    path('receipts', views.ProcessReceiptListView.as_view(), name='receipt-list'),
    path('receipts/<str:receipt_id>', views.ProcessReceiptListView.as_view(), name='receipt-detail'),
]