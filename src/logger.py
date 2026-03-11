import logging
import sys
from src.path import PASTA_LOGS

def configurar_logger(nome="RoboLogger"):
    logger = logging.getLogger(nome)
    
    # Evita duplicar logs
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.INFO)
    
    # Formato da mensagem: Data - Nível - Mensagem
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    #Salva o histórico
    arquivo_log = PASTA_LOGS / "execucao_robo.log"
    file_handler = logging.FileHandler(arquivo_log, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # Exibe na tela
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger