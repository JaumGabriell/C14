import pandas as pd

db = pd.read_csv('data.csv')

print("Mostra as duas últimas linhas:")
print(db.tail(2))

print("Tabela toda")
print(db)

print("Mostra as primeiras linhas:")
print(db.head())
