# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 20:42:02 2019

@author: mazzi
"""

# Desafio Dom Rock
# Input:
#
# Tabela MovtoITEM.xlsx
#   - item / tipo_movimento / data_lançamento / quantidade / valor
# Tabela SaldoITEM.xlsx
#   - item / data_inicio / qtd_inicio / valor_inicio / data_final / qtd_final / valor_final
#
# Output:
# Tabela result_python.csv
# Com Dados de quantidade e Valor para Entrada, Saida, Saldo inicial
# e Saldo final para cada item a cada dia

# Import packages
import pandas as pd

# Carregar dados...
df_MovtoITEM_all = pd.read_excel('../data/MovtoITEM.xlsx')
df_SaldoITEM_all = pd.read_excel('../data/SaldoITEM.xlsx')


aggs = {}
aggs['quantidade'] = ['sum']
aggs['valor'] = ['sum']

df_grouped = df_MovtoITEM_all.groupby(['item','data_lancamento','tipo_movimento']).agg(aggs)

dict_output = {}
idx_output = 0
for id_group in df_grouped.index.values:
    item = id_group[0]
    day = id_group[1]
    type_mov = id_group[2]
    
    data_row = df_grouped.loc[id_group]
    
    qtd = data_row['quantidade']['sum']
    valor = data_row['valor']['sum']
    
    dict_output[idx_output]=[item,day,type_mov,qtd,valor]
    idx_output+=1
    
df_full = pd.DataFrame.from_dict(dict_output, orient='index',
                                 columns=['item','data','tipo_movimento',
                                          'quantidade','valor'])

df_ent = df_full[df_full['tipo_movimento']=='Ent'].rename(
        columns={'quantidade':'quantidade_ent','valor':'valor_ent'})

df_sai = df_full[df_full['tipo_movimento']=='Sai'].rename(
        columns={'quantidade':'quantidade_sai','valor':'valor_sai'})

df_output = pd.merge(df_ent,df_sai, on=['item','data'],how='outer')
df_output.fillna(0,inplace=True)
del df_output['tipo_movimento_x'],df_output['tipo_movimento_y']

df_output['saldo_dia_qtd']=df_output['quantidade_ent']-df_output['quantidade_sai']
df_output['saldo_dia_valor']=df_output['valor_ent']-df_output['valor_sai']

df_output['saldo_inicial_qtd'] = 0
df_output['saldo_final_qtd'] = 0
df_output['saldo_inicial_valor'] = 0
df_output['saldo_final_valor'] = 0

for item in df_output['item'].unique():
    df_item = df_output[df_output['item']==item]
    df_item = df_item.sort_values(by=['data'])
    qtd_inicio = float(df_SaldoITEM_all[df_SaldoITEM_all['item']==item]['qtd_inicio'])
    valor_inicio = float(df_SaldoITEM_all[df_SaldoITEM_all['item']==item]['valor_inicio'])
    
    df_item_saldo_final_qtd = (df_item['saldo_dia_qtd'].cumsum()+qtd_inicio)
    
    df_item_saldo_final_valor = (df_item['saldo_dia_valor'].cumsum()+valor_inicio)
    
    df_output.loc[df_item_saldo_final_qtd.index,'saldo_final_qtd'] = df_item_saldo_final_qtd
    df_output.loc[df_item_saldo_final_valor.index,'saldo_final_valor'] = df_item_saldo_final_valor
    
    item_saldo_inicial_qtd = [qtd_inicio]+list(df_item_saldo_final_qtd.values)
    item_saldo_inicial_qtd = item_saldo_inicial_qtd[0:-1]
    
    item_saldo_inicial_valor = [valor_inicio]+list(df_item_saldo_final_valor.values)
    item_saldo_inicial_valor = item_saldo_inicial_valor[0:-1]
    
    df_output.loc[df_item_saldo_final_qtd.index,'saldo_inicial_qtd'] = item_saldo_inicial_qtd
    df_output.loc[df_item_saldo_final_valor.index,'saldo_inicial_valor'] = item_saldo_inicial_valor
    

df_output['data'] = df_output['data'].dt.strftime('%d/%m/%Y')
del df_output['saldo_dia_qtd'],df_output['saldo_dia_valor']

df_output.to_csv('../output/result_python_2.csv', index=False)

