# Importando bibliotecas 
import os # Para o leitura de aquivo CSV
import machine # Para o hasp
import time # Para o controle de tempo de leitura
import dht # Para o sensor dht11
import network # Para a conexão wi-fi

# Login e senha do WI-FI
login_wi_fi = 'RNS'
senha_wi_fi = 'VaiFuncionar'
     
# Conexão wifi --- tem que testar no rasp          
def conecta_wifi():
    wlan = network.WLAN(network.STA_IF) # Declarando conexão
    wlan.active(True) # Ativando conexão
    wlan.connect(login_wi_fi, senha_wi_fi) # Usando login e senha
    while not wlan.isconnected(): # Enquanto não conectar 
        time.sleep(1) # Espera um segundo  
    print('WiFi conectado:', wlan.ifconfig())

# Definindo onde está o sensor  
sensor = dht.DHT11(machine.Pin(4)) # Pino 4

# Arquivo para salvar dados temporários
nome_arquivo = 'data_logger.csv'

# Lendo informações de umidade e de temperatura
def ler_umidade_temperatura():
    sensor.measure() # realiza a leitura do sensor 
    umidade = sensor.humidity() # Pega dados de umidade em porcentagem
    temperatura = sensor.temperature() # Pega dados de temperatura em Celsius
    return umidade,temperatura # Retorna umidade e temperatura

# Função para criar o arquivo CSV e salvar os dados de umidade e temperatura
def salvar_dados_umidade_temperatura():
    try:
        if not arquivo_existe(nome_arquivo): # Se o arquivo não existe
            # Cria o arquivo e adiciona cabeçalhos
            with open(nome_arquivo, 'w') as arquivo:
                arquivo.write('umidade,temperatura,status,data,hora\n')
        
        with open(nome_arquivo, 'a') as arquivo:
            # Capturar a data e a hora atual (data da Leitura)
            data_hora = time.localtime()
            data_leitura = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(data_hora[0], data_hora[1], data_hora[2],data_hora[3], data_hora[4], data_hora[5])
            
            umidade_temperatura = int(ler_umidade_temperatura()) # Le o valor da umidade e da temperatura
            #status = pegar_status(umidade_temperatura)

            # Salvar os dados no arquivo CSV
            arquivo.write('{},{},{}\n'.format(umidade_temperatura[0],umidade_temperatura[1], data_leitura))
            
            # Printando para vizualizar
            print(f'Dados salvos:\n Umidade: {umidade_temperatura[0]}\n Temperatura: {umidade_temperatura[1]}\n Data da Leitura {data_leitura}')
            
    # Em caso de erro mostra mensagem        
    except OSError as e:
        print("Erro ao ler o sensor: ", e)
        #status = "ERRO"

# Função para verificar se o arquivo CSV já existe
def arquivo_existe(nome_arquivo):
    return nome_arquivo in os.listdir()

# Função para ler os dados do arquivo CSV
def ler_dados_csv():
    # Se o arquivo existe
    if arquivo_existe(nome_arquivo):
        # Printa todos os registros
        with open(nome_arquivo, 'r') as arquivo:
            print(arquivo.read())    
    else: # Caso não exista
        # Mostra mensagem
        print("Arquivo não encontrado.")

# Função para eliminar o arquivo CSV
def eliminar_arquivo_csv():
    # Se encontrar arquivo
    if arquivo_existe(nome_arquivo):
        # Apaga o arquivo
        os.remove(nome_arquivo)
        print(f"Arquivo {nome_arquivo} eliminado.")  
    else: # Se não encontrar arquivo mostra mensagem   
        print("Arquivo não encontrado para eliminação.")   
'''
# Verificar com professor como funciona com as duas entradas, umidade e temperatura
def pegar_status(umidade_temperatura_percentual):
    
    status = None 
    if umidade_temperatura_percentual >= 0 and umidade_temperatura_percentual <= 30:
        status = 'seco'
    
    elif umidade_temperatura_percentual >= 30 and umidade_temperatura_percentual <= 70:
        status = 'moderado'
        
    elif umidade_temperatura_percentual > 70 and umidade_temperatura_percentual <= 100:
        status = 'úmido'
        
    return status
'''
# Iniciando programa
while True:
    salvar_dados_umidade_temperatura() # Salvando dados do sensor
    time.sleep(10)  # Esperar 10 segundos para nova leitura
    # Fazendo leitura
    print(' ')
    ler_dados_csv()
