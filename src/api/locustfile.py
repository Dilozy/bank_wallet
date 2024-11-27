"""
Модуль предназначен для тестов API под высокой нагрузкой с помощью пакета Locust
"""

from locust import HttpUser, task, between


class WalletLoadTest(HttpUser):
    wait_time = between(1, 2)  # Интервал между запросами
    
    @task
    def perform_wallet_operations(self):
        wallet_uuid = "db10f381-c868-43aa-b84e-87c8f0e54b74"
        
        # Пример запроса на пополнение
        self.client.patch(f"/api/v1/wallets/{wallet_uuid}/operation/", json={
            "operationType": "DEPOSIT",
            "amount": 100
        })

        # Пример запроса на снятие
        self.client.patch(f"/api/v1/wallets/{wallet_uuid}/operation/", json={
            "operationType": "WITHDRAW",
            "amount": 50
        })