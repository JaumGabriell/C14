import pandas as pd

db = pd.read_csv('data.csv')

print("mostra as duas últimas linhas:")
print(db.tail(2))

print("tabela toda")
print(db)