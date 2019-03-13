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
import numpy as np

# Essa função serve para comparar dois números
# pois no python dois números flutuantes idênticos podem
# ser considerado diferentes entre si.
def comp_numero(a, b, rel_tol=1e-09, abs_tol=0.0):
    return True if abs(a-b) < rel_tol else False

# Carregar dados...
df_MovtoITEM_all = pd.read_excel('../data/MovtoITEM.xlsx')
df_SaldoITEM_all = pd.read_excel('../data/SaldoITEM.xlsx')


# Pegar todos os items
items = df_MovtoITEM_all['item'].unique()

# Lista Para armazenar todas as linhas
all_output_data = []

# Para cada item...
for item in items:
    # Carregar dados da tabela SaldoITEM para item
    data_inicio = df_SaldoITEM_all[df_SaldoITEM_all['item']==item]['data_inicio']
    qtd_inicio = df_SaldoITEM_all[df_SaldoITEM_all['item']==item]['qtd_inicio']
    valor_inicio = df_SaldoITEM_all[df_SaldoITEM_all['item']==item]['valor_inicio']
    data_final = df_SaldoITEM_all[df_SaldoITEM_all['item']==item]['data_final']
    qtd_final = df_SaldoITEM_all[df_SaldoITEM_all['item']==item]['qtd_final']
    valor_final = df_SaldoITEM_all[df_SaldoITEM_all['item']==item]['valor_final']
    
    # DataFrame com informações de movimentação para item
    df_MovtoITEM_single = df_MovtoITEM_all[df_MovtoITEM_all['item']==item]
    # List of unique dates for that item
    lista_dias = df_MovtoITEM_single['data_lancamento'].unique()
    # Organizar a lista em ordem crescente
    lista_dias = np.sort(lista_dias)
    
    
    # Saldo inicial é qtd_inicio e valor_inicio
    saldo_inicio_valor = valor_inicio.values[0]
    saldo_inicio_quant = qtd_inicio.values[0]
    
    # Loop para cada dia, em ordem crescente
    for dia in lista_dias:
        # Lista com valores para output
        lista_output = []
        """Adicionar item"""
        lista_output.append(str(item))
        """Adicionar data_lancamento"""
        lista_output.append(str(pd.to_datetime(dia).strftime('%d/%m/%Y')))
        
        # DataFrame com movimentações do dia
        df_mov_item_dia = df_MovtoITEM_single[df_MovtoITEM_single['data_lancamento']==dia]
        
        # DataFrames com dados de entrada e saida para o dia
        entrada = df_mov_item_dia[df_mov_item_dia['tipo_movimento']=='Ent']
        saida = df_mov_item_dia[df_mov_item_dia['tipo_movimento']=='Sai']
        
        # Quantidades e valores de entrada, soma dos dados
        entrada_quant = entrada['quantidade'].sum()
        entrada_valor = entrada['valor'].sum()
        
        # Quantidades e valores de saida, soma dos dados
        saida_quant = saida['quantidade'].sum()
        saida_valor = saida['valor'].sum()
        
        # Fórmula de saldo final: saldo_final = saldo_inicio + entrada - saída
        saldo_final_valor = saldo_inicio_valor + entrada_valor - saida_valor
        saldo_final_quant = saldo_inicio_quant + entrada_quant - saida_quant
        
        """Adicionar lanc_Ent_qtd"""
        lista_output.append(entrada_quant)
        """Adicionar lanc_Ent_valor"""
        lista_output.append(entrada_valor)
        """Adicionar lanc_Sai_qtd"""
        lista_output.append(saida_quant)
        """Adicionar lanc_Sai_valor"""
        lista_output.append(saida_valor)
        """Adicionar saldo_inicio_valor"""
        lista_output.append(saldo_inicio_valor)
        """Adicionar saldo_inicio_qtd"""
        lista_output.append(saldo_inicio_quant)
        """Adicionar saldo_final_valor"""
        lista_output.append(saldo_final_valor)
        """Adicionar saldo_final_qtd"""
        lista_output.append(saldo_final_quant)
        
        # Salvar dados na lista de saida
        all_output_data.append(lista_output)
        
        # Prova real:  no último dia (data_final), saldo_final_valor = valor_final
        # e saldo_final_quant = qtd_final
        if (dia==data_final.values[0]):
            if not (comp_numero(saldo_final_valor,valor_final.values[0]) & 
                comp_numero(saldo_final_quant,qtd_final.values[0])):
                print('O sistema apresenta erro')
                
        # Atualizar saldos iniciais
        saldo_inicio_valor = saldo_final_valor
        saldo_inicio_quant = saldo_final_quant
        
# DataFrame com os dados de output
output_df = pd.DataFrame(all_output_data,
                         columns=['item','data_lancamento','lanc_Ent_qtd','lanc_Ent_valor',
                                  'lanc_Sai_qtd','lanc_Sai_valor','saldo_inicio_valor',
                                  'saldo_inicio_qtd','saldo_final_valor','saldo_final_qtd'])      
    
output_df.to_csv('../output/result_python.csv',index=False)
    


