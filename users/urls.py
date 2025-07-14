from django.urls import include, path
from .views import (
     HomeView, LoginView, LogoutView, RegisterPageView, DashboardView,
    RegisterView, OTPVerifyView, ScheduledEmailViewSet, UpdateProfilePictureView, UserDetailView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from users import views
router = DefaultRouter()
router.register(r'scheduled-emails', ScheduledEmailViewSet, basename='scheduled-email')

urlpatterns = [
    # HTML Pages
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterPageView.as_view(), name='register-page'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('schedule-email/', views.schedule_email_view, name='schedule_email'),
    path('view-emails/', views.view_emails_view, name='view_emails'),

    # APIs
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/verify-otp/', OTPVerifyView.as_view(), name='api-verify-otp'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', LoginView.as_view(), name='custom_token_obtain_pair'),
    path('profile-picture/', UpdateProfilePictureView.as_view(), name='update_profile_picture'),
    path('user/', UserDetailView.as_view(), name='user_detail'),

   
    path('api/', include(router.urls)),

    path('api/logout', LogoutView.as_view(), name='logout'),


]
