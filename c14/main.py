import pandas as pd

db = pd.read_csv('data.csv')

print("mostra a última linha:")
print(db.tail())

print("tabela toda")
print(db)