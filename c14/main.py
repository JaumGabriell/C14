import pandas as pd

db = pd.read_csv('data.csv')

print("Mostra a última linha:")
print(db.tail())

print("Tabela toda")
print(db)