from pynubank import Nubank
import json
from os import listdir

print(listdir())

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
        # qr = money_request['qr_code']
        # print(qr.make_image())
        # print(qr.)
        return money_request['payment_code']


# nu = Nubank()
# nu.authenticate_with_cert(credentials["cpf"], credentials["senha"], 'cert.p12') # Essa linha funciona porque não estamos chamando o servidor do Nubank ;)

# t_id = nu.get_account_feed()[0]["id"]
# print(nu.get_pix_details(t_id))
