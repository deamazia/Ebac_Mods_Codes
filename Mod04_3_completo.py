#!/usr/bin/env python
# coding: utf-8

# # Tarefa 03
# 
# - Leia os enunciados com atenção
# - Saiba que pode haver mais de uma resposta correta
# - Insira novas células de código sempre que achar necessário
# - Em caso de dúvidas, procure os Tutores
# - Divirta-se :)

# In[3]:


import pandas as pd
import requests


# ####  1) Lendo de APIs
# Vimos em aula como carregar dados públicos do governo através de um API (*Application Programming Interface*). No exemplo de aula, baixamos os dados de pedidos de verificação de limites (PVL) realizados por estados, e selecionamos apenas aqueles referentes ao estado de São Paulo.
# 
# 1. Repita os mesmos passos feitos em aula, mas selecione os PVLs realizados por municípios no estado do Rio de Janeiro.
# 2. Quais são os três *status* das solicitações mais frequentes na base? Quais são suas frequências?
# 3. Construa uma nova variável que contenha o ano do **status**. Observe que ```data_status``` vem como tipo *object* no **DataFrame**. Dica: você pode usar o método ```.str``` para transformar o tipo da variável em string, em seguida um método como [**slice()**](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.slice.html) ou [**split()**](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.split.html).
# 4. Indique a frequência de cada ano do campo construído no item (3).

# In[9]:


url = 'http://apidatalake.tesouro.gov.br/ords/sadipem/tt/pvl?&tipo_interessado=Município&uf=RJ'


# In[10]:


r =requests.get(url)


# In[11]:


r.status_code


# In[14]:


data_json = r.json()


# In[15]:


print(data_json)


# In[29]:


pd.DataFrame(data_json['items'])


# In[30]:


df = pd.DataFrame(data_json['items'])


# In[36]:


if 'status' in df.columns:
    status_counts = df['status'].value_counts()

    print("Três status mais frequentes e suas frequências:")
    print(status_counts.head(3))


# In[33]:


df['ano_status'] = df['data_status'].str[:4]

print(df[['data_status', 'ano_status']].head())


# In[38]:


if 'ano_status' in df.columns:
    
    frequencia_anos = df['ano_status'].value_counts().sort_index().reset_index()
    frequencia_anos.columns = ['Ano', 'Frequência']

    print("Frequência de solicitações por ano:")
    print(frequencia_anos)


# #### 2) Melhorando a interação com o API
# Observe dois URLs de consultas diferentes, por exemplo o URL utilizado em aula, e o URL feito no exercício anterior. Compare-os e observe as diferenças.
# 
# 1. Faça uma função em Python que recebe como argumento o UF da consulta e o tipo de interessado (```'Estado'```ou ```Município```), e que devolve os dados da consulta no formato *DataFrame*.
# 2. Quantas solicitações para o Estado podem ser consultadas para Minas Gerais com *status* em 'Arquivado por decurso de prazo' estão registradas?
# 3. Qual é o município da Bahia com mais solicitações deferidas?
# 4. Salve um arquivo .csv com os dados de solicitações da Bahia, com interessado = 'Estado'

# In[46]:


def consultar_pvl(uf: str, tipo_interessado: str) -> pd.DataFrame:
    """
    Consulta os dados de PVL para uma UF e tipo de interessado específicos.

    Parâmetros:
    - uf (str): Sigla da unidade federativa (ex: 'RJ', 'SP').
    - tipo_interessado (str): Tipo de interessado ('Estado' ou 'Município').

    Retorna:
    - pd.DataFrame: DataFrame contendo os dados da consulta.
    """
  
    url = (
        "http://apidatalake.tesouro.gov.br/ords/sadipem/tt/pvl"
        f"?tipo_interessado={tipo_interessado}&uf={uf}"
    )


    response = requests.get(url)

    
    if response.status_code == 200:
        data_json = response.json()
        
        if 'items' in data_json:
            df = pd.DataFrame(data_json['items'])
            return df
        else:
            raise ValueError("A resposta da API não contém a chave 'items'.")
    else:
        raise ConnectionError(f"Erro na requisição: {response.status_code}")


# In[47]:


df_mg_estado = consultar_pvl('MG', 'Estado')

if 'status' in df_mg_estado.columns:
  
    arquivados = df_mg_estado[df_mg_estado['status'] == 'Arquivado por decurso de prazo']
    
    print(f"Número de solicitações arquivadas por decurso de prazo: {len(arquivados)}")
else:
    print("A coluna 'status' não foi encontrada no DataFrame.")


# In[44]:


df_bahia_municipios = consultar_pvl('BA', 'Município')

deferidos_bahia = df_bahia_municipios[
    (df_bahia_municipios['uf'] == 'BA') &
    (df_bahia_municipios['tipo_interessado'] == 'Município') &
    (df_bahia_municipios['status'] == 'Deferido')
]

solicitacoes_por_municipio = deferidos_bahia['interessado'].value_counts()

municipio_mais_solicitacoes = solicitacoes_por_municipio.idxmax()
numero_solicitacoes = solicitacoes_por_municipio.max()

print(f"O município da Bahia com mais solicitações deferidas é {municipio_mais_solicitacoes} com {numero_solicitacoes} solicitações.")



# In[45]:


df_bahia_estado = df_bahia_municipios[
    (df_bahia_municipios['uf'] == 'BA') &
    (df_bahia_municipios['tipo_interessado'] == 'Estado')
]

df_bahia_estado.to_csv('solicitacoes_bahia_estado.csv', index=False, encoding='utf-8')

