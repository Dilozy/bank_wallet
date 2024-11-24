import decimal
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import BankWallet


class WalletOperationsTestCase(TestCase):
    def setUp(self) -> None:
        self.wallet = BankWallet.objects.create(balance=1000)

    def test_deposit_operation(self) -> None:
        self.wallet.balance += 500
        self.wallet.save()
        self.assertEqual(self.wallet.balance, 1500)

    def test_withdraw_operation(self) -> None:
        self.wallet.balance -= 200
        self.wallet.save()
        self.assertEqual(self.wallet.balance, 800)


class EndpointsTestCase(APITestCase):
    def setUp(self) -> None:
        self.wallet = BankWallet.objects.create(balance=2000)
        self.url = f"/api/v1/wallets/{self.wallet.id}/"
        self.non_existent_wallet_id = "3858abcd-c52c-4f8f-975d-7556faad945d"
    
    def test_show_balance_endpoint_response(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(decimal.Decimal(response.data["balance"]), decimal.Decimal(2000))

    def test_wallet_withdraw_endpoint_response(self) -> None:
        response = self.client.post(self.url + "operation/",
                                    {"operationType": "WITHDRAW", "amount": decimal.Decimal(100)},
                                    format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"wallet_id": str(self.wallet.id),
                                         "balance": decimal.Decimal(1900),
                                         "message": "WITHDRAW of 100.00 completed successfully."})

    def test_wallet_deposit_endpoint_response(self) -> None:
        response = self.client.post(self.url + "operation/",
                                    {"operationType": "DEPOSIT", "amount": decimal.Decimal(100)},
                                    format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"wallet_id": str(self.wallet.id),
                                         "balance": decimal.Decimal(2100),
                                         "message": "DEPOSIT of 100.00 completed successfully."})
    
    def test_withdraw_insufficient_funds(self) -> None:
        response = self.client.post(self.url + "operation/",
                                    {"operationType": "WITHDRAW", "amount": decimal.Decimal(2500)},
                                    format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["details"], "Insufficient funds for withdrawal.")


    def test_negative_amount(self) -> None:
        response = self.client.post(self.url + "operation/",
                                    {"operationType": "DEPOSIT", "amount": decimal.Decimal(-100)},
                                    format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["amount"]["details"]), "The amount cannot be a negative number.")


    def test_wallet_not_found(self) -> None:
        url = f"/api/v1/wallets/{self.non_existent_wallet_id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(str(response.data["detail"]), f"Wallet with id {self.non_existent_wallet_id} not found.")

    def test_operation_with_non_existent_wallet(self) -> None:
        url = f"/api/v1/wallets/{self.non_existent_wallet_id}/"
        
        response = self.client.post(url + "operation/",
                                    {"operationType": "DEPOSIT", "amount": decimal.Decimal(100)},
                                    format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(str(response.data["detail"]), f"Wallet with id {self.non_existent_wallet_id} not found.")
