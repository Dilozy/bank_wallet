import decimal
from django.db import transaction
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.exceptions import ValidationError, NotFound
from .serializers import WalletOperationSerializer, WalletInfoSerializer
from .models import BankWallet, Transaction


class ShowWalletInfoAPI(RetrieveAPIView):
    """
    API View для отображения информации о балансе на счету
    """
    serializer_class = WalletInfoSerializer
    lookup_url_kwarg = "wallet_uuid"
    lookup_field = "id"

    def get_object(self) -> BankWallet:
        try:
            return BankWallet.objects.get(id=self.kwargs.get(self.lookup_url_kwarg))
        except BankWallet.DoesNotExist as exc:
            raise NotFound({"detail": f"Wallet with id {self.kwargs.get(self.lookup_url_kwarg)} not found."}) from exc


class ProceedWalletOperationAPI(GenericAPIView):
    """
    API View отвечающая за увеличение и уменьшениe баланса на счету
    """
    serializer_class = WalletOperationSerializer
    lookup_url_kwarg = "wallet_uuid"
    lookup_field = "id"


    def post(self, request, *args, **kwargs) -> Response:
        """
        Метод, отвечающий за выполнение операций над счетом. 
        Базируется на HTTP-методе POST
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        operation_type = serializer.validated_data["operationType"]
        amount = decimal.Decimal(serializer.validated_data["amount"])

        with transaction.atomic():
            # добавляем транзакции, чтобы данные коммитились в таблицу только при отсутствии ошибок
            try:
                # Используем select_for_update для блокировки строки
                wallet = BankWallet.objects.select_for_update().get(id=self.kwargs.get(self.lookup_url_kwarg))
            except BankWallet.DoesNotExist as exc:
                raise NotFound({"detail": f"Wallet with id {self.kwargs.get(self.lookup_url_kwarg)} not found."}) from exc
            
            if operation_type == "DEPOSIT":
                wallet.balance += amount
            elif operation_type == "WITHDRAW":
                if wallet.balance < amount:
                    raise ValidationError({
                                            "details": "Insufficient funds for withdrawal.",
                                            "current_balance": wallet.balance,
                                            "requested_amount": amount
                                        })
                wallet.balance -= amount
            
            wallet.save()

            # сохраняем в отдельной таблице информацию о совершенной транзакции
            Transaction.objects.create(
                wallet=wallet,
                operation_type=operation_type,
                amount=amount

            )

        return Response({
            "wallet_id": str(wallet.id),
            "balance": wallet.balance,
            "message": f"{operation_type} of {amount} completed successfully."
        })