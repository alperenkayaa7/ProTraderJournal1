import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from journal.models import Account, Trade
import logging
import uuid

logger = logging.getLogger(__name__)

class TradeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.account = Account.objects.create(
            account_name="Test Account",
            account_balance=1000.00,
            account_r=1.00,
            owner=self.user
        )

    def test_create_trade(self):
        url = reverse('trade-list')  # API endpoint for trade creation
        data = {
            "account": str(self.account.id),  # UUID'yi stringe çeviriyoruz
            "ticker": "EURUSD",
            "entry_price": 1.0353095,
            "stop_price": 1.0300000,
            "tp_price": 1.0400000,
            "trade_type": "BUY",
            "risk_r": 1.0,
            "quantity": 10000
        }

        response = self.client.post(url, data, content_type="application/json")
        
        # Loglama yerine print kullanımı
        print(f"Test create trade response status: {response.status_code}")
        print(f"Test create trade response content: {response.content}")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Trade.objects.count(), 1)
        trade = Trade.objects.first()
        self.assertEqual(trade.ticker, "EURUSD")
        self.assertEqual(trade.entry_price, 1.0353095)
        self.assertEqual(trade.stop_price, 1.0300000)
        self.assertEqual(trade.tp_price, 1.0400000)
        self.assertEqual(trade.trade_type, "BUY")
        self.assertEqual(trade.risk_r, 1.0)
        self.assertEqual(trade.quantity, 10000)
