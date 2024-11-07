# Importando bibliotecas 
import os # Para o leitura de aquivo CSV
import time # Para o controle de tempo de leitura
import network # Para a conexão wi-fi
import urequests as requests
import dht #Para o sensor dht11
import machine # Para o hasp

BASE_URL_POST_SYNC = "http://127.0.0.1:8000/v1/save"
BASE_URL_POST_CSV = "http://127.0.0.1:8000/v1/save_csv"
headers = {'Content-Type': 'application/json'}

# Login e senha do WI-FI
wifi_login = 'RNS'
wifi_password = 'VaiFuncionar'

# Arquivo para salvar dados temporários
file_name = 'data_logger.csv'
     
# Conexão wifi --- tem que testar no rasp          
def connect_wifi():
    wlan = network.WLAN(network.STA_IF) # Declarando conexão
    wlan.active(True) # Ativando conexão
    wlan.connect(wifi_login, wifi_password) # Usando login e senha
    while not wlan.isconnected(): # Enquanto não conectar 
        print("Conectando...")
        time.sleep(1) # Espera um segundo  
    print('WiFi conectado:', wlan.ifconfig())

# Função para verificar a conexão Wi-Fi
def is_connected():
    wlan = network.WLAN(network.STA_IF)
    return wlan.isconnected()

# Definindo onde está o sensor  
sensor = dht.DHT11(machine.Pin(26))
print(sensor)

# Lendo informações de umidade e de temperatura
def read_humidity_temperature():
    try:
        sensor.measure() # realiza a leitura do sensor 
        time.sleep(0.5)
        humidity = sensor.humidity() # Pega dados de umidade em porcentagem
        temperature = sensor.temperature() # Pega dados de temperatura em Celsius
        print(humidity, temperature)
        return humidity, temperature # Retorna umidade e temperatura
    except OSError as e:
        print("Erro ao ler o sensor:", e)
        time.sleep(1)  # Espera um segundo antes de tentar novamente
        return None, None  # Retorna valores nulos em caso de erro

# Função para criar o arquivo CSV e salvar os dados de umidade e temperatura
def save_humidity_temperature_data():
    try:
        if not file_exists(file_name): # Se o arquivo não existe
            with open(file_name, 'w') as file:
                file.write('umidade,temperatura,status,data,hora\n')
        
        with open(file_name, 'a') as file:
            # Capturar a data e a hora atual (data da Leitura)
            date_time = time.localtime()
            reading_date = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(date_time[0], date_time[1], date_time[2],date_time[3], date_time[4], date_time[5])
            
            humidity_temperature = read_humidity_temperature() # Le o valor da umidade e da temperatura
            #status = pegar_status(umidade_temperatura)
          # Verifica se a leitura foi bem-sucedida
            if humidity_temperature[0] is not None and humidity_temperature[1] is not None:
                # Salvar os dados no arquivo CSV
                file.write('{},{},{}\n'.format(humidity_temperature[0], humidity_temperature[1], reading_date))
                
                # Printando para visualizar
                print(f'Dados salvos:\n Umidade: {humidity_temperature[0]}\n Temperatura: {humidity_temperature[1]}\n Data da Leitura {reading_date}')         
            else:
                print("Leitura do sensor falhou, dados não salvos.")
    except OSError as e:
        print("Erro ao salvar os dados no CSV: ", e)
        #status = "ERRO"

# Função para verificar se o arquivo CSV já existe
def file_exists(file_name):
    return file_name in os.listdir()

# Função para ler os dados do arquivo CSV
def read_csv_data():
    # Se o arquivo existe
    if file_exists(file_name):
        # Printa todos os registros
        with open(file_name, 'r') as file:
            print(file.read())    
    else: # Caso não exista
        # Mostra mensagem
        print("Arquivo não encontrado.")

# Função para eliminar o arquivo CSV
def delete_csv_file():
    # Se encontrar arquivo
    if file_exists(file_name):
        # Apaga o arquivo
        os.remove(file_name)
        print(f"Arquivo {file_name} eliminado.")  
    else: # Se não encontrar arquivo mostra mensagem   
        print("Arquivo não encontrado para eliminação.")   

def send_data_sync():
    try:        
        humidity, temperature = read_humidity_temperature()
        data = {
                "humidity": humidity,
                "temperature": temperature,
                "collection_time": "",  
                "network_reconnect": None,  
                "network_disconnect": None
               }
           
        print(data)  
        response = requests.post(BASE_URL_POST_SYNC, json=data, headers=headers)
        
        if response.status_code == 200:
            print('Dados enviados com sucesso!')
        else:
            print('Erro ao enviar dados:', response.status_code)
        response.close()
    except Exception as e:
        print('Erro ao enviar dados:', e)

# Função para enviar dados do CSV quando a conexão for restabelecida
def send_csv_data():
    if file_exists(file_name):
        with open(file_name, 'r') as file:
            data = file.read()
        response = requests.post(BASE_URL_POST_CSV, headers=headers, data=data, timeout=10)
        if response.status_code == 200:
            print('Dados do CSV enviados com sucesso!')
            delete_csv_file() # Remove o arquivo após o envio
        else:
            print('Erro ao enviar dados do CSV:', response.status_code)

# Iniciando programa
connect_wifi()
while True:
    humidity_temperature = read_humidity_temperature()  # Lê os dados do sensor
    if is_connected():  # Verifica se está conectado ao Wi-Fi
        send_data_sync()  # Envia os dados imediatamente
    else:
        save_humidity_temperature_data()  # Salvando dados do sensor
        time.sleep(10)  # Esperar 10 segundos para nova leitura
        send_csv_data()  # Tenta enviar dados do CSV se a conexão for restabelecida

    print(' ')
    read_csv_data()
