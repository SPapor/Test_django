from rest_framework import generics
from .models import Client, Deal
from .serializers import ClientSerializer, DealSerializer


class ClientListAPI(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class DealListAPI(generics.ListAPIView):
    serializer_class = DealSerializer

    def get_queryset(self):
        queryset = Deal.objects.all()
        status_param = self.request.query_params.get('status')

        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset