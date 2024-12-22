from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
import threading

# Configuração do Selenium (modo headless)
def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

# Função para assistir a um único vídeo
def assistir_video(link):
    driver = setup_driver()
    try:
        driver.get(link)
        time.sleep(random.uniform(3, 5))  # Aguarde o carregamento inicial
        video_duration = driver.execute_script("return document.querySelector('video').duration")
        print(f"Assistindo vídeo de {video_duration} segundos.")
        time.sleep(video_duration)  # Assiste ao vídeo completo
        print(f"Vídeo assistido: {link}")
    except Exception as e:
        print(f"Erro ao assistir o vídeo {link}: {e}")
    finally:
        driver.quit()

# Função para calcular o tempo e os dias necessários
def calcular_tempo(horas_desejadas, duracao_total_segundos):
    total_segundos = horas_desejadas * 3600
    repeticoes = total_segundos / duracao_total_segundos
    return repeticoes

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Envie os links dos vídeos do YouTube separados por espaços ou em uma lista, junto com a quantidade de horas desejadas (exemplo: 4000)."
    )

# Receber links e horas desejadas
async def processar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        mensagem = update.message.text
        partes = mensagem.splitlines()  # Divide a mensagem em linhas
        links = [parte.strip() for parte in partes if parte.startswith("http")]

        if not links:
            await update.message.reply_text("Por favor, envie ao menos um link de vídeo.")
            return

        # Extrai o número de horas desejadas
        horas_desejadas = None
        for linha in partes:
            try:
                horas_desejadas = int(linha.strip())
                break
            except ValueError:
                continue

        if horas_desejadas is None:
            await update.message.reply_text("Por favor, envie também a quantidade de horas desejadas como um número.")
            return

        # Simular duração de vídeos (cada vídeo com 16 minutos, por exemplo)
        duracao_total_segundos = len(links) * 16 * 60

        # Calcular repetição e tempo
        repeticoes = calcular_tempo(horas_desejadas, duracao_total_segundos)
        dias_necessarios = repeticoes / 3  # Limite de 3 execuções por dia

        resposta = (
            f"Para atingir {horas_desejadas} horas assistidas com {len(links)} vídeos:\n"
            f"- Você precisará assistir aos vídeos {int(repeticoes)} vezes.\n"
            f"- Isso levará aproximadamente {int(dias_necessarios)} dias, assistindo 3 vezes ao dia.\n"
        )

        # Aviso sobre penalidade no YouTube
        aviso = (
            "\u26A0\ufe0f *Importante*: Para evitar penalidades no YouTube, execute o bot no máximo 3 vezes por dia, "
            "com pausas de pelo menos 6 a 8 horas entre as execuções.\n"
            "Evite comportamentos repetitivos excessivos para manter sua conta segura."
        )
        resposta += aviso

        await update.message.reply_text(resposta, parse_mode="Markdown")

        # Informa o início do processo
        await update.message.reply_text("O processo de assistir os vídeos foi iniciado. Aguarde enquanto os vídeos são executados.")

        # Inicia a automação em outra thread
        threading.Thread(target=executar_automacao, args=(links,)).start()

    except Exception as e:
        await update.message.reply_text(f"Erro: {e}")

# Função para assistir vídeos
def executar_automacao(links):
    for link in links:
        assistir_video(link)
        time.sleep(random.uniform(5, 10))  # Pausa entre os vídeos

# Configurar o bot
def main():
    api_key = "7705193101:AAFiereuwtKfY0ipBVSdTDixwDtHHdQIyOo"
    application = ApplicationBuilder().token(api_key).build()

    # Adicionar comandos e handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_mensagem))

    # Iniciar o bot
    application.run_polling()

if __name__ == "__main__":
    main()
