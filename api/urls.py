from django.urls import path
from .views import LandDetailList, LandDetailDetail
from .views import LandSearchViewList, LandMapViewSetList, LandMapSingleAPIView, UserPofileViewSet, RegisterUserView, LogoutViewSet



urlpatterns = [
    path('land-details/', LandDetailList.as_view(), name='land-detail-list'),

    path('land-details/<int:pk>/', LandDetailDetail.as_view(), name='land-detail-detail'),


    path('map-url/<int:pk>/', LandMapSingleAPIView.as_view(), name='land-map-url'),

    path('land-page-display/', LandSearchViewList.as_view({'get': 'list'}), name='land-search-list'),

    path('land-map/',LandMapViewSetList.as_view({'get': 'list', 'post': 'create'}), name='land-map-view'),
  

    path('admin/profile/', UserPofileViewSet.as_view({'get':'list','put':'update'}), name='profile'),

    path('admin/register/', RegisterUserView.as_view(), name='register-user'),

    path('admin/logout/', LogoutViewSet.as_view({'post': 'create'}), name='logout'),

    # path('dashboarduser/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
   
   
]