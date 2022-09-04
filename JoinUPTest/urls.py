from django.urls import path, include

urlpatterns = [
    path("api/v1/", include("JoinUPTest.api.v1.urls")),
    path('__debug__/', include('debug_toolbar.urls')),
]
