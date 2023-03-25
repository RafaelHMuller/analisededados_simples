#!/usr/bin/env python
# coding: utf-8

# # Exercício - Mini Projeto de Análise de Dados
# 
# Temos os dados de 2019 de uma empresa de prestação de serviços. 
# 
# - Cadastro de Funcionarios
# - Cadastro de Clientes
# - Base de Serviços Prestados
# 
# ### O que queremos saber/fazer?
# 
# 1. O Total da Folha Salarial   
#     
# 2. O faturamento da empresa    
#     
# 3. O % de funcionários que já fechou algum contrato
#     
# 4. O total de contratos que cada área da empresa já fechou
# 
# 5. O total de funcionários por área
# 
# 6. O ticket médio mensal (faturamento médio mensal) dos contratos

# In[12]:


#1 - importar a base de dados
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

clientes = pd.read_csv('CadastroClientes.csv', sep=',', encoding = 'ISO-8859-1')
funcionarios = pd.read_csv('CadastroFuncionarios.csv', sep=';')
servicos = pd.read_excel('BaseServiçosPrestados.xlsx')

display(clientes)
clientes.info()
display(funcionarios)
funcionarios.info()
display(servicos)
servicos.info()


# In[2]:


#2 - tratamento dos dados
clientes[['ID Cliente', 'Nome Cliente', 'Valor Contrato Mensal', 'NaN']] = clientes['ID Cliente\tCliente\tValor Contrato Mensal\tNaN'].str.split('\t', expand=True)
clientes = clientes.drop('ID Cliente\tCliente\tValor Contrato Mensal\tNaN', axis=1)
clientes = clientes.drop('NaN', axis=1)
clientes[['ID Cliente', 'Valor Contrato Mensal']] = clientes[['ID Cliente','Valor Contrato Mensal']].astype('int')
display(clientes)
clientes.info()
                     
funcionarios['Impostos'] = funcionarios['Impostos'].str.replace(',', '.')
funcionarios['Beneficios'] = funcionarios['Beneficios'].str.replace(',', '.')
funcionarios['VR'] = funcionarios['VR'].str.replace(',', '.')
funcionarios[['Impostos', 'Beneficios', 'VR']] = funcionarios[['Impostos', 'Beneficios', 'VR']].astype('float')
display(funcionarios)
funcionarios.info()


# In[3]:


#3 - Total da Folha Salarial
funcionarios['Salário Bruto'] = funcionarios['Salario Base'] + funcionarios['Impostos'] + funcionarios['Beneficios'] + funcionarios['VT'] + funcionarios['VR']
display(funcionarios)


# In[4]:


#4 - faturamento da empresa
df1 = clientes[['ID Cliente', 'Valor Contrato Mensal']].merge(servicos[['ID Cliente', 'Tempo Total de Contrato (Meses)']], on='ID Cliente')
df1['Valor Total Contrato'] = df1['Valor Contrato Mensal'] * df1['Tempo Total de Contrato (Meses)']
display(df1)

faturamento = df1['Valor Total Contrato'].sum()
print(f'O faturamento total é de R$ {faturamento:,.2f}.')

#5 - lucro líquido da empresa
folha = funcionarios['Salário Bruto'].sum()
lucroliquido = faturamento - folha
print(f'O lucro líquido é de R$ {lucroliquido:,.2f}.')


# In[5]:


#6 - percentual de funcionários que já fechou algum contrato (apresentar a lista)
func = servicos['ID Funcionário'].unique()
percent = len(func) / len(funcionarios)
print(f'O percentual de funcionários que já fechou algum contrato é de {percent:.1%}.\n')

lista_nomes = []
for i, idfuncionario in enumerate(func):
    if idfuncionario in funcionarios['ID Funcionário']:
        nomes = funcionarios['Nome Completo'][i]
        lista_nomes.append(nomes)
        
print(f'Funcionários: {lista_nomes}')


# In[21]:


#7 - total de contratos que cada área da empresa já fechou (gráfico comparativo)
df2 = servicos[['ID Funcionário']].merge(funcionarios[['ID Funcionário', 'Area']], on='ID Funcionário')

df2_f = len(df2.loc[df2['Area']=='Financeiro', 'Area'])
df2_l = len(df2.loc[df2['Area']=='Logística', 'Area'])
df2_o = len(df2.loc[df2['Area']=='Operações', 'Area'])
df2_a = len(df2.loc[df2['Area']=='Administrativo', 'Area'])
df2_c = len(df2.loc[df2['Area']=='Comercial', 'Area'])
lista_areas = [df2_f, df2_l, df2_o, df2_a, df2_c]

print(f'''Financeiro: {df2_f},
Logística: {df2_l},
Operações: {df2_o},
Administrativo: {df2_a},
Comercial: {df2_c}
''')

    #outra maneira de fazer
df2_qtdes = df2['Area'].value_counts()
df2_qtdesss = pd.DataFrame(df2_qtdes)
print(df2_qtdesss)


# In[14]:


#gráfico (plotly)
fig = px.bar(df2_qtdesss, y=df2_qtdesss['Area'], title='Número de contratos fechados por área',
             text_auto=True, labels={'Area':'Quantidade de contratos fechados'})
fig.update_traces(textfont_size=20, textangle=0, textposition="inside", cliponaxis=False)
fig.update_traces(marker_color='rgb(255,100,200)')
fig.show()


# In[25]:


# gráfico (matplotlib/seaborn)
plt.figure(figsize=(10,5))
plt.title('Número de contratos fechados por área')
sns.barplot(data=df2_qtdesss, y=df2_qtdesss['Area'], x=df2_qtdesss.index)


# In[7]:


#6 - total de funcionários por área (gráfico comparativo)
df3 = funcionarios[['ID Funcionário', 'Area']]
display(df3)

df3_qtde = df3['Area'].value_counts()
df3_qtdeee = pd.DataFrame(df3_qtde)
df3_qtdeee = df3_qtdeee.reset_index()
display(df3_qtdeee)

#gráfico
fig = px.pie(df3_qtdeee, values = df3_qtdeee['Area'], names = df3_qtdeee['index'], title='Número de funcionários por área')
fig.update_traces(textfont_size=15, textposition="inside", textinfo='percent+label')
#fig.update_traces(marker_color='rgb(0,0,0)')
fig.show()


# In[8]:


#7 - faturamento médio mensal dos contratos
media = clientes['Valor Contrato Mensal'].mean()
print(f'Valor médio R$ {media:,.2f}')


# In[9]:


#8 - maior contrato da empresa em valor
maior_mensal = clientes['Valor Contrato Mensal'].max()
print(f'Maior valor mensal de contrato R$ {maior_mensal:,.2f}')

maior_total = df1['Valor Total Contrato'].max()
print(f'Maior valor total de contrato R$ {maior_total:,.2f}')


# In[10]:


#9 - criar uma nova planilha com toda a base de dados 
df4 = clientes.merge(servicos, on='ID Cliente')
df5 = df4.merge(funcionarios, on='ID Funcionário')
display(df5)

df5.to_excel('Planilha final.xlsx', index=False)


# In[ ]:




