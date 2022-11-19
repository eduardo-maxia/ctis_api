from django.contrib.auth.models import User, Group
from .utils.nubank import NubankClient
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pessoa, AlunoPagameto
from .serializers import UserSerializer, GroupSerializer, PessoaSerializer, AlunoPagamentoSerializer
from rest_framework import viewsets
from django import get_version
from django.views.generic import TemplateView
from .tasks import show_hello_world
from .models import DemoModel
import requests
import json
from datetime import datetime, timezone
# Create your views here.


class ShowHelloWorld(TemplateView):
    template_name = 'hello_world.html'

    def get(self, *args, **kwargs):
        show_hello_world.apply()
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['demo_content'] = DemoModel.objects.all()
        context['version'] = get_version()
        return context


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PessoaView(APIView):
    def get_object(self, pk):
        try:
            return Pessoa.objects.get(pk=pk)
        except Pessoa.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        _pessoa = self.get_object(pk)
        return Response(
            data=PessoaSerializer(_pessoa).data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        # 1 - Parse input:
        _dict_inputs = {el[0]: el[1][0] for el in {**request.data}.items()}
        # 2 - Create the User:
        _user = User(username=_dict_inputs['telefone'], password='12345678')
        _user.save()

        _pessoa = Pessoa(user_id=_user.id, **_dict_inputs)
        _pessoa.save()
        return Response(
            data=PessoaSerializer(_pessoa).data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        _pessoa = self.get_object(pk)
        _pessoa.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class AlunoPagamentoView(APIView):
    pix_identifier_prefix = 'ctispagamento'

    def get_object(self, pk):
        try:
            return AlunoPagameto.objects.get(pk=pk)
        except AlunoPagameto.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        _pessoa = Pessoa.objects.get(user_id=request.user.id)

        # INDEX
        if pk is None:
            all_payments = AlunoPagameto.objects.filter(
                pessoa_aluno_id=_pessoa.id).all()

            # Active User
            if len(all_payments) > 0:
                # Check if this month's payment has been issued
                last_payment = 0
                for payment in all_payments:
                    last_payment = max(last_payment, payment.mes_referencia)
                for month in range(last_payment + 1, datetime.now(timezone.utc).month + 1):
                    novo_pagamento = AlunoPagameto(
                        pessoa_aluno_id=_pessoa.id,
                        mes_referencia=month,
                        valor=5
                    )
                    novo_pagamento.save()

                # Update status for all payments
                nu = NubankClient()
                nu.update_all_status(self.pix_identifier_prefix)

            # First time user
            else:
                print('first timer')

            all_payments = AlunoPagameto.objects.filter(
                pessoa_aluno_id=_pessoa.id).all()

            return Response(
                data=[
                    AlunoPagamentoSerializer(payment).data
                    for payment in all_payments],
                status=status.HTTP_200_OK
            )

        # SHOW
        pagamento = self.get_object(pk)

        response = requests.post(
            'https://pix.ae',
            params={
                "tipo": "cpf",
                "chave": "082.822.014-05",
                "nome": "Eduardo dos Anjos Rodrigu",
                "valor": "10.00",
                "info": f"{_pessoa.nome} - {pagamento.mes_referencia}",
                "txid": f"{self.pix_identifier_prefix}{pagamento.id}"
            },
            headers={
                "accept": "application/json",
                "content-type": "application/json"
            },
            timeout=5000
        )
        pagamento.link = json.loads(response.text)['qrstring']
        pagamento.save()

        return Response(
            data=AlunoPagamentoSerializer(pagamento).data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        _pessoa = Pessoa.objects.get(user_id=request.user.id)

        for mes in range(1, 12):
            novo_pagamento = AlunoPagameto(
                pessoa_aluno_id=_pessoa.id,
                mes_referencia=mes,
                valor=115
            )
            novo_pagamento.save()

        return Response(
            data=AlunoPagamentoSerializer(novo_pagamento).data,
            status=status.HTTP_200_OK
        )
