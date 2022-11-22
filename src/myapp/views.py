from django.contrib.auth.models import User, Group
from .utils.nubank import NubankClient
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pessoa, TurmaAlunoPagamento, TurmaAluno, Mes, Configuracoes, Turma
from .serializers import UserSerializer, GroupSerializer, PessoaSerializer, TurmaAlunoPagamentoSerializer, TurmaSerializer, TurmaAlunoSerializer
from rest_framework import viewsets
from django import get_version
from django.views.generic import TemplateView
from .tasks import show_hello_world
from .models import DemoModel
import requests
import json
from datetime import datetime, timezone
from .utils.expo_notifications import send_notification
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

    def get(self, request, pk=None):
        _pessoa = Pessoa.objects.get(user = request.user.id) if pk is None else self.get_object(pk)
        _user = User.objects.get(pk = request.user.id)
        _is_password_initial = _user.check_password('123456')
        return Response(
            data=PessoaSerializer(_pessoa).data | {'is_password_initial': _is_password_initial},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        # 1 - Parse input:
        _dict_inputs = {el[0]: el[1][0] for el in {**request.data}.items()}
        # 2 - Create the User:
        _user = User.objects.create_user(username=_dict_inputs.pop('telefone'), password='123456')
        _user.save()

        _pessoa = Pessoa(user_id=_user.id, **_dict_inputs)
        _pessoa.save()
        return Response(
            data=PessoaSerializer(_pessoa).data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk=None):
        _pessoa = Pessoa.objects.get(user = request.user.id) if pk is None else self.get_object(pk)
        if request.data.get('expoPushToken') is not None:
            _pessoa.expoPushToken = request.data['expoPushToken']
            _pessoa.save()
        if request.data.get('password') is not None:
            _user = User.objects.get(pk=request.user.id)
            if not _user.check_password(request.data['password_old']):
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED
                )
            _user.set_password(request.data['password'])
            _user.save()
        if request.data.get('reset_password') is not None:
            _user = User.objects.get(pk=request.data.get('reset_password'))
            _user.set_password('123456')
            _user.save()
        if request.data.get('data_vencimento') is not None:
            _pessoa.data_vencimento = request.data['data_vencimento']
            _pessoa.save()
        if request.data.get('telefone') is not None:
            _user = User.objects.get(pk = request.user.id)
            _user.username = request.data['telefone']
            _user.save()
        return Response(
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        _pessoa = self.get_object(pk)
        _pessoa.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class TurmaView(APIView):
    def get_object(self, pk):
        try:
            return Turma.objects.get(pk=pk)
        except Pessoa.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        # INDEX
        if pk is None:
            _all_turmas = Turma.objects.all()
            return Response(
                data=[{
                    **TurmaSerializer(turma).data,
                    'tipo_dias': turma.tipo_dias_serialized(),
                    'professor': turma.pessoa_professor.nome,
                    'sede': turma.sede.nome,
                    'alunos': [{
                        **TurmaAlunoSerializer(aluno).data,
                        **PessoaSerializer(aluno.pessoa_aluno).data
                    } for aluno in TurmaAluno.objects.filter(turma = turma).all()]
                } for turma in _all_turmas],
                status=status.HTTP_200_OK
            )

        return Response(
            data={
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        _dict_inputs = {el[0]: el[1][0] for el in {**request.data}.items()}

        _turma = Turma(**_dict_inputs)
        _turma.save()
        return Response(
            data=TurmaSerializer(_turma).data,
            status=status.HTTP_200_OK
        )

class TurmaAlunoView(APIView):
    def get_object(self, pk):
        try:
            return Turma.objects.get(pk=pk)
        except Pessoa.DoesNotExist:
            raise Http404

    def post(self, request):
        _dict_inputs = {el[0]: el[1][0] for el in {**request.data}.items()}

        _turma = TurmaAluno(**_dict_inputs)
        _turma.save()
        return Response(
            data=TurmaAlunoSerializer(_turma).data,
            status=status.HTTP_200_OK
        )

class TurmaAlunoPagamentoView(APIView):
    pix_identifier_prefix = 'ctispagamento'

    def get_object(self, pk):
        try:
            return TurmaAlunoPagamento.objects.get(pk=pk)
        except TurmaAlunoPagamento.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        _pessoa = Pessoa.objects.get(user_id=request.user.id)
        current_date = datetime.now(timezone.utc)

        # INDEX
        if pk is None:
            all_payments = TurmaAlunoPagamento.objects.select_related('turma_aluno').filter(turma_aluno__pessoa_aluno_id = _pessoa.id).all()

            # Active User
            if len(all_payments) > 0:
                # Get last issued payment
                last_payment = 0
                for payment in all_payments:
                    last_payment = max(last_payment, payment.mes_referencia.id)
                    # Update payment status based on date
                    if payment.status in [1,2]:
                        if payment.mes_referencia.id > current_date.month:
                            continue
                        if _pessoa.data_vencimento and _pessoa.data_vencimento > current_date.day:
                            payment.status = 2
                            continue
                        payment.status = 3
                        payment.save()

                # Check if this month's payment has been issued
                # for month in range(last_payment + 1, current_date.month + 1):
                #     novo_pagamento = TurmaAlunoPagamento(
                #         pessoa_aluno_id=_pessoa.id,
                #         mes_referencia=month,
                #         valor=5
                #     )
                #     novo_pagamento.save()

                # Update status for all payments
                nu = NubankClient()
                nu.process_all_transactions(self.pix_identifier_prefix)

            # First time user
            else:
                print('first timer')

            all_payments = TurmaAlunoPagamento.objects.select_related('turma_aluno').filter(turma_aluno__pessoa_aluno_id = _pessoa.id).all()

            return Response(
                data=[
                    {
                        **TurmaAlunoPagamentoSerializer(pagamento).data,
                        'mes': pagamento.mes_referencia.mes_serialized(),
                        'status': pagamento.status_serialized()
                    }
                    for pagamento in all_payments],
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
                "info": f"{_pessoa.nome} - {pagamento.mes_referencia.mes_serialized()}",
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
            data={
                **TurmaAlunoPagamentoSerializer(pagamento).data,
                'mes': pagamento.mes_referencia.mes_serialized(),
                'status': pagamento.status_serialized()
            },
            status=status.HTTP_200_OK
        )

    # def post(self, request):
    #     _pessoa = Pessoa.objects.get(user_id=request.user.id)

    #     for mes in range(1, 12):
    #         novo_pagamento = TurmaAlunoPagamento(
    #             pessoa_aluno_id=_pessoa.id,
    #             mes_referencia=mes,
    #             valor=115
    #         )
    #         novo_pagamento.save()

    #     return Response(
    #         data=TurmaAlunoPagamentoSerializer(novo_pagamento).data,
    #         status=status.HTTP_200_OK
    #     )

class NotificacaoView(APIView):
    def post(self, request):
        # _pessoa = Pessoa.objects.get(user_id=request.user.id)
        current_date = datetime.now(timezone.utc)

        # Mandar notficação de dia de pagamento
        if request.data.get('data_vencimento'):
            _mes_referencia = Mes.objects.get(mes = current_date.month, ano_letivo = current_date.year)
            _pagamentos_pendentes = TurmaAlunoPagamento.objects.select_related('turma_aluno__pessoa_aluno').filter(
                status__in = [1,2,3], mes_referencia = _mes_referencia,
                turma_aluno__pessoa_aluno__data_vencimento = request.data.get('data_vencimento')).all()
            
            _notificacoes = [
                {
                    'to': _pagamento_pendente.turma_aluno.pessoa_aluno.expoPushToken,
                    'title': 'CUIDAAAAAA',
                    'body': 'Bora pagar',
                    'subtitle': 'Tá no teu dia de vencimento',
                    'data': {'pagamento_id': _pagamento_pendente.id},
                    'badge': 1
                }
            for _pagamento_pendente in _pagamentos_pendentes]

            send_notification(_notificacoes)

        if request.data.get('title'):
            _pessoas = Pessoa.objects.all()
            _notificacoes = [
                {
                    'to': pessoa.expoPushToken,
                    'title': request.data.get('title'),
                    'body': request.data.get('body'),
                    'subtitle': request.data.get('subtitle'),
                    'badge': 1
                }
            for pessoa in _pessoas if pessoa.expoPushToken is not None]

            send_notification(_notificacoes)

        return Response(
            data={
                # **TurmaAlunoPagamentoSerializer(pagamento).data,
                # 'mes': pagamento.mes_referencia.mes_serialized(),
                # 'status': pagamento.status_serialized()
            },
            status=status.HTTP_200_OK
        )
