#!/usr/bin/env python
# coding: utf-8

# ## Exercício 1: Vestibular
# 
# Considere que a os dados gerados na célula abaixo contêm o número de acertos de 100 alunos em um vestibular para um curso de exatas, divididas pelos respectivos assuntos. Considere que cada assunto possui um número de questões conforme a tabela abaixo:
# 
# | assunto | número de questões |
# |:---:|:---:|
# | Matemática | 24 |
# | Português | 18 |
# | Geografia | 8 |
# | Inglês | 8 |
# | História | 8 |
# | Física | 12 |
# | Química | 12 |
# 
# Usando os comandos de operações com DataFrames que você aprendeu na Aula 03, calcule:
# 
# 1. (operações com escalar) Calcule o percentual de acerto dos alunos por assunto.  
# 2. (operações entre *DataFrames) Calcule o total de acertos de cada aluno.  
# 3. Calcule o porcentual geral de cada aluno.  
# 4. Suponha que a nota de corte para a segunda fase seja 45. Quantos alunos tiveram nota maior que 45?  

# In[5]:


import pandas as pd
import numpy as np

np.random.seed(42)
df_mat = pd.DataFrame(np.random.randint(24, size=(100, 1)), columns=['Qt_acertos'])

df_por = pd.DataFrame(np.random.randint(18, size=(100, 1)), columns=['Qt_acertos'])

df_geo = pd.DataFrame(np.random.randint(8, size=(100, 1)), columns=['Qt_acertos'])

df_ing = pd.DataFrame(np.random.randint(8, size=(100, 1)), columns=['Qt_acertos'])

df_his = pd.DataFrame(np.random.randint(8, size=(100, 1)), columns=['Qt_acertos'])

df_fis = pd.DataFrame(np.random.randint(12, size=(100, 1)), columns=['Qt_acertos'])

df_qui = pd.DataFrame(np.random.randint(12, size=(100, 1)), columns=['Qt_acertos'])


# In[14]:


per_mat = df_mat.copy()
per_por = df_por.copy()
per_geo = df_geo.copy()
per_ing = df_ing.copy()
per_his = df_his.copy()
per_fis = df_fis.copy()
per_qui = df_qui.copy()

per_mat['Pct_acerto'] = (df_mat['Qt_acertos'] / 24) * 100
per_por['Pct_acerto'] = (df_por['Qt_acertos'] / 18) * 100
per_geo['Pct_acerto'] = (df_geo['Qt_acertos'] / 8) * 100
per_ing['Pct_acerto'] = (df_ing['Qt_acertos'] / 8) * 100
per_his['Pct_acerto'] = (df_his['Qt_acertos'] / 8) * 100
per_fis['Pct_acerto'] = (df_fis['Qt_acertos'] / 12) * 100
per_qui['Pct_acerto'] = (df_qui['Qt_acertos'] / 12) * 100

print('Matemática:')
print(per_mat.head())

print('\nPortuguês:')
print(per_por.head())

print('\nGeografia:')
print(per_geo.head())

print('\nInglês :')
print(per_ing.head())

print('História :')
print(per_his.head())

print('Física :')
print(per_fis.head())

print('Quimíca :')
print(per_qui.head())


# In[15]:


df_acertos = df_mat + df_por + df_geo + df_his + df_fis + df_qui

print(df_acertos.head())



# In[19]:


per_acertos = df_acertos / 90 *100

print(per_acertos.head())


# In[20]:


alunos_aprovados = per_acertos[per_acertos > 45].shape[0]

print(f'Número de alunos com nota maior que 45: {alunos_aprovados}')


# ## 2) Vestibular II
# 
# Ainda sobre o mesmo banco de dados:
# 
# 1. Neste vestibular, quem 'zera' em matemática, física ou química está desqualificado. Monte um novo *DataFrame* com os alunos desqualificados por este critério.
# 2. Quantos são esses alunos?
# 3. Qual a média desses alunos em história e geografia?
# 4. Monte um *DataFrame* com os alunos que passaram para a segunda fase. Repare que estes alunos não podem ter sido desqualificados.

# In[24]:


desqualificados = df_acertos[(df_mat['Qt_acertos'] == 0) | (df_fis['Qt_acertos'] == 0) | (df_qui['Qt_acertos'] == 0)]

print(f'Número de alunos desqualificados: {desqualificados.shape[0]}')



# In[25]:


media_his_geo = desqualificados[['Qt_acertos']].join(df_his[['Qt_acertos']].rename(columns={'Qt_acertos': 'His'})).join(df_geo[['Qt_acertos']].rename(columns={'Qt_acertos': 'Geo'}))
media_his_geo = media_his_geo[['His', 'Geo']].mean(axis=1)
print('Média dos desqualificados em História e Geografia:')
print(media_his_geo.head())




# In[29]:


alunos_aprovados = per_acertos[per_acertos > 45]

df_segunda_fase = alunos_aprovados[~alunos_aprovados.index.isin(desqualificados.index)]

print(f'Número de alunos que passaram para a segunda fase: {df_segunda_fase.shape[0]}')


# ## 3) Vacinações no Acre
# Vamos trabalhar agora com a base de vacinações no Acre. Para facilitar a sua vida, copiamos o link do arquivo na célula abaixo.
# 
# 1. Quantas vacinas estão registradas nessa base?  
# 2. Quantos pacientes foram vacinados? (considere um paciente para cada valor único de ```paciente_id```)  
# 3. Quantos pacientes únicos tomaram a primeira dose? OBS: Há um caractere especial neste campo. Receba os valores do campo com o método ```.unique()```.   
# 4. Quantos pacientes com menos de 18 anos foram vacinados?  
# 5. Quantos estabelecimentos aplicaram vacina no Acre?
# 
# 
# **OBS:** O portal do DATASUS pode apresentar instabilidades, retornando um erro na segunda célula abaixo. Por este motivo está disponível uma base estática, que se for baixada para o seu *working directory* pode ser lida com este comando: ```df = pd.read_csv('registros de vacinacao covid ACRE.csv', sep=';')```.
# 
# **OBS2:** Para saber qual é o seu working directory, rode no jupyter: ```!pwd```.

# In[9]:


arquivo = 'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SIPNI/COVID/uf/uf%3DAC/part-00000-5ed92752-6121-474f-ab37-816918134afc.c000.csv'


# In[10]:


import pandas as pd

arquivo_local = r'C:\Users\Shinoki\Downloads\vacina_covid_acre.csv'

df = pd.read_csv(arquivo_local, sep=';')

print(df.head())


# In[11]:


vacinas_registradas = df['vacina_nome'].nunique()

print(f'Número de vacinas registradas: {vacinas_registradas}')



# In[12]:


pacientes_vacinados = df['paciente_id'].nunique()

print(f'Número de pacientes vacinados: {pacientes_vacinados}')


# In[23]:


df['vacina_descricao_dose'] = df['vacina_descricao_dose'].str.replace('\xa0', ' ', regex=True)
df['vacina_descricao_dose'] = df['vacina_descricao_dose'].str.strip()

print(df['vacina_descricao_dose'].unique())





# In[24]:


primeira_dose = df[df['vacina_descricao_dose'] == '1ª Dose']

pacientes_primeira_dose = primeira_dose['paciente_id'].nunique()

print(f"Número de pacientes únicos que tomaram a 1ª dose: {pacientes_primeira_dose}")



# In[25]:


menores_18 = df[df['paciente_idade'] < 18]

pacientes_menores_18 = menores_18['paciente_id'].nunique()

print(f"Número de pacientes com menos de 18 anos vacinados: {pacientes_menores_18}")



# In[26]:


num_estabelecimentos = df['estabelecimento_valor'].nunique()

print(f"Número de estabelecimentos que aplicaram vacina no Acre: {num_estabelecimentos}")


# ## 4) Vacinação II
# Gere um *DataFrame* que contenha somente os estabelecimentos que aplicaram vcinas a menores de 18 anos. Nesse *DataFrame* devem conter somente os dados dos estabelecimentos, mais uma coluna sendo a quantidade de vacinas que o estabelecimento aplicou a menores de 18 anos.  
#   
# 1. crie uma cópia do *DataFrame* original, contendo somente os registros de vacinas realizadas a menores de 18 anos.  
# 2. crie uma lista das colunas desse *DataFrame* com o atributo de *DataFrame* **.columns()**  
# 3. Nesse *DataFrame* faça uma contagem do campo ```vacina_categoria_nome```.
# 3. a partir da lista de colunas, escolha somente aquelas que são referentes ao estabelecimento, faça uma lista com esses valores.  
# 4. usando o método *.loc*, selecione somente essas variáveis  
# 5. Aplique o método **.drop_duplicates** e crie uma lista com uma linha para cada estabelecimento, com os dados do estabelecimento  

# In[28]:


df_estabelecimentos_menores = (
    df[df['paciente_idade'] < 18]
    .groupby([
        'estabelecimento_valor',
        'estabelecimento_razaosocial',
        'estalecimento_nofantasia',
        'estabelecimento_municipio_codigo',
        'estabelecimento_municipio_nome',
        'estabelecimento_uf'
    ])
    .size()
    .reset_index(name='quantidade_vacinas_menores')
)



# In[29]:


df_menores = df[df['paciente_idade'] < 18].copy()



# In[30]:


lista_colunas = df_menores.columns.tolist()



# In[31]:


contagem_categorias = df_menores['vacina_categoria_nome'].value_counts()
print(contagem_categorias)



# In[32]:


colunas_estabelecimento = [
    'estabelecimento_valor',
    'estabelecimento_razaosocial',
    'estalecimento_nofantasia',
    'estabelecimento_municipio_codigo',
    'estabelecimento_municipio_nome',
    'estabelecimento_uf'
]



# In[33]:


df_estabelecimentos_info = df_estabelecimentos_menores.loc[:, colunas_estabelecimento]

print(df_estabelecimentos_info.head())



# In[35]:


df_unicos_estabelecimentos = df_estabelecimentos_info.drop_duplicates()
lista_estabelecimentos = df_unicos_estabelecimentos.to_dict(orient='records')

print(lista_estabelecimentos[:5])  


# In[ ]:




