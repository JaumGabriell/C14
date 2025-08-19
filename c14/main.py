import pandas as pd

db = pd.read_csv('data.csv')

print("Amostra aleatória:")
print(db.sample())

print("Tabela toda")
print(db)