from uuid import uuid4

from django.db import models


class BankWallet(models.Model):
    """
    ORM-Модель банковского счета
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4)
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Текущий баланс")

    def __str__(self) -> str:
        return f"Wallet {self.id} - Balance {self.balance}"


class Transaction(models.Model):
    """
    ORM-Модель для фиксации успешно проведенных транзакций
    """
    
    operation_choices = [
        ("DEPOSIT", "Deposit"),
        ("WITHDRAW", "Withdraw"),
    ]
    
    wallet = models.ForeignKey(BankWallet, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=10, choices=operation_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.operation_type} - {self.amount} ({self.wallet.id})"