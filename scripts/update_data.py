from upload_data import get_engine_conn
from sqlalchemy import select, column, text
import pandas as pd

engine, conn = get_engine_conn()

id_col = column('estacoes_id')

query_limno = select(id_col, column('chla')).select_from(text('limnologia')).where(id_col.like('Ibitinga%'))
limno_result = conn.execute(query_limno).fetchall()

query_aphy = select(text('*')).select_from(text('aphy_mean')).where(id_col.like('Ibitinga%'))
aphy_result = conn.execute(query_aphy).fetchall()

aphy_df = pd.DataFrame(aphy_result, columns=['id', 'estacoes_id'] + [f'x{wavelength}' for wavelength in range(220, 801)])

aphy_df.set_index('id', inplace=True)

aphy_new = aphy_df.copy()

numeric_cols = aphy_new.select_dtypes(include='number').columns
for row in limno_result:
    line, value = row[0], row[1]

    mask = aphy_new['estacoes_id'] == line
    aphy_new.loc[mask, numeric_cols] = aphy_new.loc[mask, numeric_cols].apply(lambda x: x * value)

for _, row in aphy_new.iterrows():
    update_query = text(f"""
        UPDATE aphy_mean
        SET {', '.join([f"{col} = :{col}" for col in numeric_cols])}
        WHERE estacoes_id = :estacoes_id
    """)

    # Criar dicionário com os valores a serem passados na query
    params = {col: row[col] for col in numeric_cols}
    params['estacoes_id'] = row['estacoes_id']

    conn.execute(update_query, params)

# Confirmar as mudanças no banco
conn.commit()

print("Atualização concluída!")
