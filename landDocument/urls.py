from django.urls import path
from .views import LandDocumentListView, LandDocumentSearchView, LandDocumentDetailView

urlpatterns =[
   path("landDocument/",LandDocumentListView.as_view(), name="transactions_list_view"),
   path("landDocument/search/",LandDocumentSearchView.as_view(),name="transactions_search_view"),
   path("landDocument/<int:id>/", LandDocumentDetailView.as_view(), name="transactions_detail_view"),
]