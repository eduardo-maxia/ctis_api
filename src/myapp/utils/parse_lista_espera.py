import pandas as pd
data = pd.read_fwf('lista de espera.txt', header=None)
x = data.to_numpy()[0][0][-1]
v = data.to_numpy()[3][0][-1]
lista = [el[0] for el in data.to_numpy() if x not in el[0] and v not in el[0]]
pd.DataFrame(lista).to_excel('Lista de espera.xlsx')