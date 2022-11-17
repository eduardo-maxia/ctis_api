from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from ctis_api.serializers import UserSerializer, GroupSerializer, PessoaSerializer, AlunoPagamentoSerializer
from ctis_api.models import Pessoa, AlunoPagameto
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ctis_api.utils.nubank import NubankClient


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PessoaView(APIView):
    def get(self, request):
        return Response(
            data=PessoaSerializer(
                Pessoa.objects.get(user_id=request.user.id)).data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        p = Pessoa(user_id=request.user.id, cpf='08282201405', data_vencimento=5,
                   nome='Eduardo', status=1, telefone='(21)93618-1803')
        p.save()
        return Response(
            data=PessoaSerializer(p).data,
            status=status.HTTP_200_OK
        )


class AlunoPagamentoView(APIView):
    def get(self, request):

        all_payments = AlunoPagameto.objects.filter(pessoa_aluno_id=10).all()
        
        return Response(
            data=[
                AlunoPagamentoSerializer(payment).data
            for payment in all_payments],
            status=status.HTTP_200_OK
        )

    def post(self, request):
        pessoa = Pessoa.objects.get(id = 10)

        nu = NubankClient()

        for mes in range(1,12):
            novo_pagamento = AlunoPagameto(
                pessoa_aluno_id = pessoa.id,
                mes_referencia = mes,
                valor = 115
            )
            novo_pagamento.save()
            novo_pagamento.link = nu.create_pix_payment(novo_pagamento.id)
            novo_pagamento.save()

        return Response(
            data=AlunoPagamentoSerializer(novo_pagamento).data,
            status=status.HTTP_200_OK
        )
