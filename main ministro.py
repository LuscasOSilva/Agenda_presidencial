from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

# Pegar todas as últimas 3 datas
x = 3
datas = [(datetime.now() - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(1,x+1)]

# Configurações do WebDriver (Chrome)
service = Service()

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

# URL da agenda do ministro da fazenda
url_ministro = 'https://eagendas.cgu.gov.br/?_token=nbon4g1pDJJ1M3ctj9HjjkGDScw35P4xGcqJsl7j&filtro_orgaos_ativos=on&filtro_orgao=1384&filtro_cargos_ativos=on&filtro_cargo=MINISTRO%28A%29+DA+FAZENDA&filtro_apos_ativos=on&filtro_servidor=14641&cargo_confianca_id=&is_cargo_vago=false#divcalendar'

# Iniciar o navegador e abrir a página
driver.get(url_ministro)

# Dicionário para armazenar eventos por data
agenda_por_data = {}

# Encontrar todos os elementos <td> com o atributo data-date
tds = driver.find_elements(By.TAG_NAME, 'td')

# Filtrar os <td> que têm o atributo 'data-date' igual às datas passadas
tds_filtrados = [td for td in tds if td.get_attribute('data-date') in datas]

# Extrair os eventos e horários dos <td> filtrados
for td in tds_filtrados:
    data = td.get_attribute('data-date')
    eventos = td.find_elements(By.CLASS_NAME, 'fc-daygrid-event-harness')

    eventos_com_horarios = []
    for evento in eventos:
        horario = evento.find_element(By.CLASS_NAME, 'fc-event-time').get_attribute('textContent') + 'h'
        titulo = evento.find_element(By.CLASS_NAME, 'fc-event-title').get_attribute('textContent')

        eventos_com_horarios.append((horario, titulo))
    
    agenda_por_data[data] = eventos_com_horarios

# Fechar o navegador
driver.quit()

'''
# Print do resultado final
for data, eventos in agenda_por_data.items():
    print(f'\nData: {data}')
    for horario, evento in eventos:
        print(f'{horario}: {evento}')
'''

# Criar uma lista de tuplas com todas as entradas da agenda
lista_eventos = [(data, horario, evento) for data, eventos in agenda_por_data.items() for horario, evento in eventos]

# Criar um DataFrame pandas com os dados
df = pd.DataFrame(lista_eventos, columns=['Data', 'Horário', 'Evento'])

# Exportar os dados para um arquivo CSV
df.to_csv('agenda_ministro_fazenda.csv', index=False)