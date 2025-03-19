import time
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import csv
import os

# Configuração do WebDriver
def iniciar_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Evita detecção como bot
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--headless")  # Remova essa linha para visualizar o carregamento

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Função para capturar temperatura e umidade do ClimaTempo
def capturar_dados():
    driver = iniciar_driver()
    url = "https://www.climatempo.com.br/previsao-do-tempo/cidade/558/saopaulo-sp"
    driver.get(url)

    # Tempo extra para carregar completamente
    time.sleep(5)

    try:
        # Capturar temperatura
        temperatura_element = driver.find_elements(By.ID, "current-weather-temperature")
        temperatura = temperatura_element[0].text if temperatura_element else "N/A"

        # Capturar umidade
        umidade_element = driver.find_elements(By.ID, "current-weather-humidity")
        umidade = umidade_element[0].text if umidade_element else "N/A"

        # Capturar data e hora atual
        agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"Temperatura: {temperatura} | Umidade: {umidade} | Data/Hora: {agora}")

        # Salvar no CSV
        salvar_csv(agora, temperatura, umidade)

    except Exception as e:
        print("Erro ao capturar dados:", e)

    finally:
        driver.quit()

# Função para salvar os dados em um arquivo CSV
def salvar_csv(data_hora, temperatura, umidade):
    arquivo_csv = "historico_clima.csv"
    arquivo_existe = os.path.isfile(arquivo_csv)

    with open(arquivo_csv, mode="a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)

        # Se o arquivo ainda não existe, criar o cabeçalho
        if not arquivo_existe:
            escritor.writerow(["Data/Hora", "Temperatura", "Umidade"])

        # Escrever os dados
        escritor.writerow([data_hora, temperatura, umidade])

# Criar interface gráfica com Tkinter
def criar_interface():
    janela = tk.Tk()
    janela.title("Previsão do tempo de São Paulo")
    janela.geometry("300x150")

    label = tk.Label(janela, text="Atualizar previsão na planilha:")
    label.pack(pady=10)

    botao = tk.Button(janela, text="Buscar previsão", command=capturar_dados)
    botao.pack(pady=5)

    janela.mainloop()

# Executar a interface gráfica
if __name__ == "__main__":
    criar_interface()
