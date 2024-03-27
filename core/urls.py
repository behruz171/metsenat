from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from apps.common.views import *
from .schema import swagger_urlpatterns
# from .views import SponsorRetrieveUpdateDestroy
from rest_framework .generics import RetrieveUpdateDestroyAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('auth/', include('apps.users.urls')),
    path('sponsor-create/',SponsorCreateAPIView.as_view()),
    path('sponsor-add/',StudentSponsorCreateAPIView.as_view()),
    path('students/<int:student_id>/allocated-amounts/', StudentSponsorListAPIView.as_view()), 
    path('students/',StudentListAPIView.as_view()),
    path('sponsors/', SponsorListAPIView.as_view()),
    path('total-amount-statistic/', TotalAmountStatisticAPIView.as_view()),
    path('monthly-statistic/',MonthlyStatisticAPIView.as_view()),
    # path('sponsor-update/<int:pk>/', SponsorRetrieveUpdateDestroy.as_view()),
    path('update-statistic/<int:pk>/', AllocatedAmountUpdateAPIView.as_view())

]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
