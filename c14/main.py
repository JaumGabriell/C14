import pandas as pd

db = pd.read_csv('data.csv')

print("amostra aleatória:")
print(db.sample())

print("tabela toda")
print(db)