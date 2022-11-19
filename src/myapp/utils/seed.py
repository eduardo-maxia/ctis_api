from ..models import Pessoa, Sede, Turma, TurmaAluno, Mes, TurmaAlunoPagamento, Configuracoes
from django.contrib.auth.models import User

# from myapp.utils.seed import seed_db

def seed_db():
    # Pessoas
    arlen = create_pessoa('85997915952', 1, 'Arlen')
    iury = create_pessoa('85985092711', 1, 'Iury')
    eduardo = create_pessoa('21936181803', 3, 'Eduardo')
    tito = create_pessoa('85996866683', 3, 'Tito')

    # Sedes
    arclo = Sede(nome='Arclo')
    arclo.save()
    sede_nova = Sede(nome='Sede Nova')
    sede_nova.save()

    # Turmas
    melhor_turma = Turma(
        sede_id = arclo.id,
        tipo_dias = 2,
        horario = '21:00',
        pessoa_professor_id = arlen.id
    )
    melhor_turma.save()

    # TurmaAlunos
    eduardo_1 = create_turma_aluno(eduardo, melhor_turma)
    iury_1 = create_turma_aluno(iury, melhor_turma)
    tito_1 = create_turma_aluno(tito, melhor_turma)

    # Meses
    for ano in [2022, 2023]:
        for mes in range(1, 13):
            _mes = Mes(ano_letivo = ano, mes = mes)
            _mes.save()

    # TurmaAlunoPagamentos
    create_pagamentos(eduardo_1)
    create_pagamentos(iury_1)
    create_pagamentos(tito_1)


    # Configuracoes
    config = Configuracoes(ano_letivo = 2022, last_transaction = '')
    config.save()


def create_pessoa(telefone, tipo, nome):
    _user =  User.objects.create_user(username = telefone, password = '123456')
    _user.save()
    _pessoa = Pessoa(
        user_id = _user.id,
        tipo_pessoa = tipo,
        nome = nome
    )
    _pessoa.save()
    return _pessoa

def create_turma_aluno(aluno, turma):
    _ta = TurmaAluno(turma_id = turma.id, pessoa_aluno_id=aluno.id)
    _ta.save()
    return _ta

def create_pagamentos(turma_aluno):
    for mes in range(6, 12):
        _tap = TurmaAlunoPagamento(
            turma_aluno_id = turma_aluno.id,
            mes_referencia_id = mes,
            valor = 10
        )
        _tap.save()
