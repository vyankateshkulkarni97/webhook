from django.urls import path
# from . import views

# urlpatterns = [
#     path('create_account/', views.create_account, name='create_account'),
#     path('create_destination/<uuid:account_id>/', views.create_destination, name='create_destination'),
#     path('handle_data/', views.handle_data, name='handle_data'),
  
# ]

from .views import AccountListCreateView, AccountRetrieveUpdateDestroyView, DestinationListCreateView, DestinationRetrieveUpdateDestroyView, get_destinations_for_account, incoming_data

urlpatterns = [
    path('accounts/', AccountListCreateView.as_view(), name='account_list_create'),
    path('accounts/<uuid:pk>/', AccountRetrieveUpdateDestroyView.as_view(), name='account_retrieve_update_destroy'),
    path('destinations/', DestinationListCreateView.as_view(), name='destination-list-create'),
    path('destinations/<uuid:pk>/', DestinationRetrieveUpdateDestroyView.as_view(), name='destination_retrieve_update_destroy'),
    path('destinations/<uuid:account_id>/', get_destinations_for_account, name='get_destinations_for_account'),
    path('incoming_data/', incoming_data, name='incoming_data'),
]