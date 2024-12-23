from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
import os
import time
import random
import threading
import requests
from fake_useragent import UserAgent

from dotenv import load_dotenv
import os
load_dotenv()
# Obter proxies dinâmicos de uma API
def get_proxy_from_api():
    response = requests.get("https://proxylist.geonode.com/api/proxy-list?limit=10&page=1&sort_by=lastChecked&sort_type=desc&protocols=http")
    if response.status_code == 200:
        proxies = response.json().get("data", [])
        if proxies:
            proxy = random.choice(proxies)
            return f"{proxy['ip']}:{proxy['port']}"
    return None

# Alternativa: Proxies estáticos
def get_static_proxy():
    proxies = [
        "192.168.1.100:8080",
        "192.168.1.101:8080",
        "192.168.1.102:8080"
    ]
    return random.choice(proxies)

# Configuração do Selenium com proxies e User-Agent
def setup_driver(proxy):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random  # Gerar um novo User-Agent aleatório

    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--headless")  # Não abre janelas
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    proxy_config = Proxy()
    proxy_config.proxy_type = ProxyType.MANUAL
    proxy_config.http_proxy = proxy
    proxy_config.ssl_proxy = proxy
    capabilities = webdriver.DesiredCapabilities.CHROME
    proxy_config.add_to_capabilities(capabilities)

    service = Service("/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options, desired_capabilities=capabilities)

# Função para assistir a um único vídeo por um período determinado
def assistir_video(link, duracao_desejada):
    print(f"Iniciando o vídeo: {link}")
    proxy = get_proxy_from_api() or get_static_proxy()
    print(f"Usando proxy: {proxy}")
    driver = setup_driver(proxy)

    try:
        driver.get(link)
        time.sleep(random.uniform(3, 5))  # Aguarde o carregamento inicial

        # Simula ações humanas como movimentar o mouse ou pressionar teclas
        driver.execute_script("window.scrollTo(0, 100);")  # Rolar para baixo
        time.sleep(random.uniform(1, 3))
        driver.execute_script("window.scrollTo(0, 0);")    # Rolar para cima

        total_assistido = 0
        while total_assistido < duracao_desejada * 3600:  # Transformar horas em segundos
            time.sleep(random.uniform(10, 20))  # Pausas aleatórias entre interações
            total_assistido += 30  # Simulando 30 segundos assistidos por iteração

        print(f"Finalizado: {link}")
    except Exception as e:
        print(f"Erro ao assistir o vídeo {link}: {e}")
    finally:
        driver.quit()

# Função para simular várias pessoas assistindo aos vídeos simultaneamente
def gerar_400_pessoas_assistindo(links, duracao_desejada):
    num_threads = 400  # Simular 400 "pessoas"
    threads = []

    for _ in range(num_threads):
        for link in links:
            thread = threading.Thread(target=assistir_video, args=(link, duracao_desejada))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

# Função para calcular a duração estimada da tarefa e o total de horas acumuladas
def calcular_duracao_e_horas(links, num_pessoas):
    total_duracao = 0  # Total da duração dos vídeos (em segundos)

    for link in links:
        try:
            driver = setup_driver(get_static_proxy())
            driver.get(link)
            time.sleep(random.uniform(3, 5))  # Aguardar carregamento inicial
            duracao = driver.execute_script("return document.querySelector('video').duration")
            total_duracao += duracao
            driver.quit()
        except Exception as e:
            print(f"Erro ao obter a duração do vídeo {link}: {e}")

    tempo_acumulado = total_duracao * num_pessoas
    horas_acumuladas = tempo_acumulado / 3600
    duracao_total_em_horas = total_duracao / 3600

    return duracao_total_em_horas, horas_acumuladas

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Envie os links dos vídeos do YouTube separados por espaços ou em uma lista, junto com a quantidade de horas desejadas (exemplo: 4000)."
    )

# Receber links e processar a tarefa
async def processar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        mensagem = update.message.text
        partes = mensagem.splitlines()
        links = [parte.strip() for parte in partes if parte.startswith("http")]

        if not links:
            await update.message.reply_text("Por favor, envie ao menos um link de vídeo.")
            return

        # Número de "pessoas" simuladas
        num_pessoas = 400

        # Calcula duração estimada e horas acumuladas
        duracao_total, horas_acumuladas = calcular_duracao_e_horas(links, num_pessoas)

        resposta = (
            f"📺 Total de vídeos: {len(links)}\n"
            f"👥 Simulações de pessoas: {num_pessoas}\n"
            f"⏳ Duração estimada da tarefa: {duracao_total:.2f} horas\n"
            f"🕒 Horas acumuladas (simulação): {horas_acumuladas:.2f} horas\n\n"
            "Iniciando a simulação de 400 pessoas assistindo aos vídeos. Por favor, aguarde..."
        )
        await update.message.reply_text(resposta)

        # Inicia a automação em outra thread
        threading.Thread(target=gerar_400_pessoas_assistindo, args=(links, duracao_total)).start()

    except Exception as e:
        await update.message.reply_text(f"Erro: {e}")

# Configurar o bot
def main():
    api_key = os.getenv("TELEGRAM_API_KEY")  # Pegando a API Key do bot de uma variável de ambiente
    if not api_key:
        print("Erro: Chave da API do Telegram não configurada!")
        return

    application = ApplicationBuilder().token(api_key).build()

    # Adicionar comandos e handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_mensagem))

    # Iniciar o bot
    application.run_polling()

if __name__ == "__main__":
    main()
