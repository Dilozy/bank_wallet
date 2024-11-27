from decimal import Decimal
from typing import Dict, Union

from rest_framework import serializers

from .models import BankWallet


class WalletOperationSerializer(serializers.Serializer):
    """
    Сериалайзер, отвечающий за обработку операций со счетом
    """
    
    operationType = serializers.ChoiceField(choices=[
        ("DEPOSIT", "Deposit"),
        ("WITHDRAW", "Withdraw"),
    
    ])
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_amount(self, value: Decimal) -> Decimal:
        # запрещаем обрабатывать отрицательные числа в операциях
        if value < 0:
            raise serializers.ValidationError({"details": "The amount cannot be a negative number."})
        return value

    def validate(self, data: Dict[str, Union[str, Decimal]]) -> Dict[str, Union[str, Decimal]]:
        if len(data) != 2 or ("operationType" not in data or "amount" not in data):
            raise serializers.ValidationError({
                    "details": "Your request format is invalid. It should be like {operationType: " ", amount: " "}"
                    })
        return data
                

class WalletInfoSerializer(serializers.ModelSerializer):
    """
    Сериалайзер данных баланса на счете
    """
    
    class Meta:
        model = BankWallet
        fields = [
            "balance"
        ]

        read_only_fields = [
            "balance"
        ]

