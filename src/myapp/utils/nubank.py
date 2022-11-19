from pynubank import Nubank
import json
from ..models import AlunoPagameto, Configuracoes

class NubankClient:
    def __init__(self) -> None:
        with open('auth/credentials.json', 'r') as f:
            credentials = json.load(f)

        self.nubank = Nubank()
        self.nubank.authenticate_with_cert(
            credentials["cpf"], credentials["senha"], 'auth/cert.p12')

        response = self.nubank.get_available_pix_keys()
        self.account_id = response['account_id']
        self.pix_key = response['keys'][0]

    def create_pix_payment(self, identifier, value=115):
        money_request = self.nubank.create_pix_payment_qrcode(
            self.account_id, value, self.pix_key, identifier)
        return money_request['payment_code']

    def update_all_status(self, pix_identifier_prefix):
        page_data = self.nubank.get_account_feed_paginated()['edges']

        # Get last processed transaction:
        config = Configuracoes.objects.get(pk=1)
        last_transaction_id = config.last_transaction

        # Set last processed transaction:
        tx_id = page_data[0]['node']['id']
        config.last_transaction = tx_id
        config.save()

        # Process all transactions until the very last one uprocessed:
        while True:
            for transaction in page_data:
                tx_id = transaction['node']['id']
                if tx_id == last_transaction_id:
                    return
                if transaction['node'].get('footer') != 'Pix' or self.nubank.get_pix_details(tx_id) is None:
                    continue

                aluno_pagamento_id = self.nubank.get_pix_details(tx_id)['id']
                if aluno_pagamento_id is None or not aluno_pagamento_id.startswith(pix_identifier_prefix):
                    continue

                _pagamento = AlunoPagameto.objects.get(pk=aluno_pagamento_id.replace(pix_identifier_prefix, ''))
                _pagamento.status = 3
                _pagamento.save()
            page_data = self.nubank.get_account_feed_paginated(cursor=page_data[0]['cursor'])['edges']
            break


# nu = Nubank()
# nu.authenticate_with_cert(credentials["cpf"], credentials["senha"], 'cert.p12') # Essa linha funciona porque não estamos chamando o servidor do Nubank ;)

# t_id = nu.get_account_feed()[0]["id"]
# print(nu.get_pix_details(t_id))
