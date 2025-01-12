import random
import requests
from selenium import webdriver
import threading
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Importação do WebDriver Manager

# Lista de proxies fornecidos no formato IP:PORT:USER:PASS
PROXIES = [
    "194.38.18.51:7113:ALICCEEE:PPROXYSS",
    "92.112.175.239:6512:ALICCEEE:PPROXYSS",
    "91.123.8.130:6670:ALICCEEE:PPROXYSS",
    "185.72.241.146:7438:ALICCEEE:PPROXYSS",
    "91.123.8.91:6631:ALICCEEE:PPROXYSS",
    "85.198.47.68:6336:ALICCEEE:PPROXYSS",
    "92.112.202.209:6793:ALICCEEE:PPROXYSS",
    "23.129.253.227:6845:ALICCEEE:PPROXYSS",
    "185.72.240.73:7109:ALICCEEE:PPROXYSS",
    "91.123.11.196:6462:ALICCEEE:PPROXYSS",
    "92.112.202.187:6771:ALICCEEE:PPROXYSS",
    "194.38.18.169:7231:ALICCEEE:PPROXYSS",
    "91.123.10.193:6735:ALICCEEE:PPROXYSS",
    "92.113.245.138:5824:ALICCEEE:PPROXYSS",
    "185.72.241.8:7300:ALICCEEE:PPROXYSS",
    "23.129.253.235:6853:ALICCEEE:PPROXYSS",
    "92.113.245.118:5804:ALICCEEE:PPROXYSS",
    "85.198.45.30:5954:ALICCEEE:PPROXYSS",
    "92.112.175.145:6418:ALICCEEE:PPROXYSS",
    "85.198.45.127:6051:ALICCEEE:PPROXYSS",
    "185.72.241.53:7345:ALICCEEE:PPROXYSS",
    "45.91.166.80:7139:ALICCEEE:PPROXYSS",
    "92.112.171.24:5992:ALICCEEE:PPROXYSS",
    "185.72.240.10:7046:ALICCEEE:PPROXYSS",
    "92.112.172.11:6283:ALICCEEE:PPROXYSS",
    "92.113.244.233:5920:ALICCEEE:PPROXYSS",
    "92.112.170.174:6143:ALICCEEE:PPROXYSS",
    "185.72.242.11:5694:ALICCEEE:PPROXYSS",
    "92.112.202.170:6754:ALICCEEE:PPROXYSS",
    "45.91.167.96:6655:ALICCEEE:PPROXYSS"
]

# Configuração do Selenium com proxies autenticados
def setup_driver(proxy):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random

    # Configuração do User-Agent
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--headless")  # Omitir a interface gráfica para performance
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Extraindo dados do proxy no formato IP:PORT:USER:PASS
    ip, port, user, password = proxy.split(":")
    proxy_url = f"http://{user}:{password}@{ip}:{port}"

    # Configurar proxy
    options.add_argument(f"--proxy-server={proxy_url}")

    # Usando o WebDriver Manager para obter o ChromeDriver
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=options)

# Simulação de assistir vídeo
def assistir_video(link, proxy, duracao_desejada):
    print(f"Iniciando o vídeo: {link} com proxy {proxy}")
    driver = setup_driver(proxy)

    try:
        driver.get(link)
        time.sleep(random.uniform(5, 10))  # Aguarda o carregamento completo da página

        # Simula interações humanas
        driver.execute_script("window.scrollTo(0, 100);")
        time.sleep(random.uniform(1, 3))
        driver.execute_script("window.scrollTo(0, 0);")

        total_assistido = 0
        while total_assistido < duracao_desejada * 3600:
            time.sleep(random.uniform(10, 20))
            total_assistido += 30

        print(f"Finalizado: {link}")
    except Exception as e:
        print(f"Erro ao assistir o vídeo {link}: {e}")
    finally:
        driver.quit()

# Simulação de 30 agentes assistindo a vídeos simultaneamente
def gerar_30_agentes_assistindo(links, duracao_desejada):
    num_threads = 30
    threads = []

    for i in range(num_threads):
        proxy = PROXIES[i % len(PROXIES)]  # Seleciona proxies ciclicamente
        link = random.choice(links)       # Escolhe aleatoriamente um link

        thread = threading.Thread(target=assistir_video, args=(link, proxy, duracao_desejada))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Exemplo de uso
if __name__ == "__main__":
    links = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=3JZ_D3ELwOQ"
    ]
    gerar_30_agentes_assistindo(links, 1),
