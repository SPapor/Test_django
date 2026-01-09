from django.test import TestCase
from django.urls import reverse
from .models import Client, Deal

class CrmTests(TestCase):
    def setUp(self):
        self.test_client = Client.objects.create(
            name="Test Company",
            phone="1234567890",
            email="test@company.com"
        )

    def test_client_creation(self):
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(self.test_client.name, "Test Company")

    def test_deal_creation(self):
        deal = Deal.objects.create(
            client=self.test_client,
            title="Super Deal",
            amount=100.00,
            status="new"
        )
        self.assertEqual(deal.client, self.test_client)
        self.assertEqual(self.test_client.deals.count(), 1)

    def test_pages_work(self):
        response = self.client.get(reverse('client_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Company")