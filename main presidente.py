from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# pegar todas as ultimas 3 datas
x = 3
datas = [(datetime.now() - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(1,x+1)][::-1]

# user agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}

# capturar urls dos ultimos 3 dias da agenda do presidente da república
urls = ['https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica-lula/agenda-do-presidente-da-republica/' + data for data in datas]

urls

# capturar as paginas dos ultimos 3 dias da agenda do presidente
pages_presidente = [requests.get(url, headers = headers) for url in urls]

# Dicionário para armazenar eventos por data
agenda_por_data_presidente = {}

# Analisar cada página com BeautifulSoup presidente
for i, page in enumerate(pages_presidente):
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Extrair horários e eventos
    horarios = [re.sub(r'h', ':', time_tag.get_text(strip=True)) + 'h' for time_tag in soup.find_all('time')]
    eventos = [h2_tag.get_text(strip=True) for h2_tag in soup.find_all('h2')]
    
    # Combinar horários e eventos
    eventos_com_horarios = list(zip(horarios, eventos))
    
    # Armazenar no dicionário com a data correspondente
    agenda_por_data_presidente[datas[i]] = eventos_com_horarios

'''
# Print do resultado final
for data, eventos in agenda_por_data_presidente.items():
    print(f'\nData: {data}')
    for horario, evento in eventos:
        print(f'{horario}: {evento}')
'''

# Criar uma lista de tuplas com todas as entradas da agenda
lista_eventos = [(data, horario, evento) for data, eventos in agenda_por_data_presidente.items() for horario, evento in eventos]

# Criar um DataFrame pandas com os dados
df = pd.DataFrame(lista_eventos, columns=['Data', 'Horário', 'Evento'])

# Exportar os dados para um arquivo CSV
df.to_csv('agenda_presidente.csv', index=False)