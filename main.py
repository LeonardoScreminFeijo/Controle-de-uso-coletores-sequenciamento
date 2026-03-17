import datetime
import time
import schedule
from src.bot import RoboNavegador
from src.logger import configurar_logger

# Define o Logger
logger = configurar_logger()

def executar_robo():
    hora_atual = datetime.datetime.now().hour
    if hora_atual >= 6:
        logger.info(">>> INICIANDO EXTRAÇÃO <<<")
    
        robo = RoboNavegador()

        try:
            robo.iniciar_driver()
            robo.login()
            arq_rotas = robo.extrair_relatorio()
            if arq_rotas:
                logger.info(f"Sucesso: {arq_rotas.name}")
            else:
                logger.error("Falha ao baixar.")
        except Exception as e:
            logger.error(f"Erro durante o ciclo: {e}")
        finally:
            robo.fechar()
    else:
        logger.info(f"Não iniciado")

if __name__ == "__main__":
    
    executar_robo()
    schedule.every(60).minutes.do(executar_robo)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1) # Espera 1 segundo para não fritar a CPU
        except KeyboardInterrupt:
            logger.info("Programa interrompido pelo usuário.")
            break
        except Exception as e:
            logger.error(f"Erro fatal no agendador: {e}")
            time.sleep(60)