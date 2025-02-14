'''
This file creates the database based on "Dados_Estatisticos.csv" with fields:
- ANO
- MES
- MERCADO
- RPK
'''

import pandas as pd
from database import db
from models import Voo, Usuario
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# load csv
df = pd.read_csv("data/Dados_Estatisticos.csv", sep=";", encoding="utf-8", skiprows=1)

# filters
# added filter to exclude rows where RPK is null
df = df[(df["EMPRESA_SIGLA"] == "GLO") & (df["GRUPO_DE_VOO"] == "REGULAR") & (df["NATUREZA"] == "DOMÉSTICA") & (df["RPK"].notna())]

# column MERCADO
df["MERCADO"] = df.apply(lambda row: "".join(sorted([str(row["AEROPORTO_DE_ORIGEM_SIGLA"]), str(row["AEROPORTO_DE_DESTINO_SIGLA"])])), axis=1)

# create dataframe
df = df[["ANO", "MES", "MERCADO", "RPK"]]

# export to db
with app.app_context():
    db.create_all()
    for _, row in df.iterrows():
        voo = Voo(ano=row["ANO"], mes=row["MES"], mercado=row["MERCADO"], rpk=row["RPK"])
        db.session.add(voo)
    db.session.commit()
