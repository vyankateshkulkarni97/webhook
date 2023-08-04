from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, ParseError, AuthenticationFailed
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
import requests

class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationListCreateView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

@api_view(['GET'])
def get_destinations_for_account(request, account_id):
    try:
        account = Account.objects.get(account_id=account_id)
    except Account.DoesNotExist:
        raise NotFound('Account not found')

    destinations = Destination.objects.filter(account=account)
    serializer = DestinationSerializer(destinations, many=True)
    return Response(serializer.data)

@api_view(['POST', 'GET'])
def incoming_data(request):
    if request.method == 'POST':
        secret_token = request.headers.get('CL-X-TOKEN')
        if not secret_token:
            raise AuthenticationFailed('Unauthenticated: Secret token not provided.')

        try:
            account = Account.objects.get(app_secret_token=secret_token)
        except Account.DoesNotExist:
            raise AuthenticationFailed('Unauthenticated: Invalid secret token.')

        data = request.data
        if not data:
            raise ParseError('Invalid Data: Data not found in request.')

        if request.method == 'GET' and not isinstance(data, dict):
            return Response({'message': 'Invalid Data'}, status=400)

        destinations = Destination.objects.filter(account=account)

        for destination in destinations:
            url = destination.url
            http_method = destination.http_method
            headers = destination.headers

            try:
                if http_method == "POST":
                    response = requests.post(url, json=data, headers=headers)
                elif http_method == "PUT":
                    response = requests.put(url, json=data, headers=headers)
                elif http_method == "GET":
                    response = requests.get(url, params=data, headers=headers)
                if response.status_code == 200:
                    print(f"Data sent successfully to {url}")
                else:
                    print(f"Failed to send data to {url}. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error sending data to {url}: {e}")

        return Response({'message': 'Data handled and sent to destinations successfully.'})

    return Response({'message': 'Use POST method to send data.'})
