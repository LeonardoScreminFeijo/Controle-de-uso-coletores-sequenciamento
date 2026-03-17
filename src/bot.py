import logging
import os
import time
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

from src.path import PASTA_DADOS, HEADLESS, RAIZ_PROJETO, URL_SITE

load_dotenv()

class RoboNavegador:
    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger("RoboLogger")

    def iniciar_driver(self):
        self.logger.info("Iniciando Chrome")
        
        opcoes = Options()
        if HEADLESS:
            opcoes.add_argument("--headless=new")
            
        
        opcoes.add_argument("--start-maximized")
        opcoes.add_argument("--disable-gpu")
        opcoes.add_argument('--ignore-certificate-errors')
        
        prefs = {
            "download.default_directory": str(PASTA_DADOS.resolve()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
            
        }
        opcoes.add_experimental_option("prefs", prefs)

        caminho_driver = RAIZ_PROJETO / "chromedriver.exe"
        
        if not caminho_driver.exists():
            raise FileNotFoundError("chromedriver.exe não encontrado na raiz!")
        
        servico = Service(executable_path=str(caminho_driver))
        self.driver = webdriver.Chrome(service=servico, options=opcoes)
        

        if HEADLESS:
            self.driver.execute_cdp_cmd('Page.setDownloadBehavior', {
                'behavior': 'allow',
                'downloadPath': str(PASTA_DADOS.resolve())
            })
        opcoes.add_argument("--start-maximized")
        opcoes.add_argument("--window-size=1920,1080")

    def fechar(self):
        if self.driver:
            self.driver.quit()
            self.logger.info("Navegador encerrado.")

    def _aguardar_download(self, timeout=60):
        self.logger.info("Aguardando download finalizar")
        fim_tempo = time.time() + timeout
        while time.time() < fim_tempo:
            arquivos = list(PASTA_DADOS.glob("*"))
            em_andamento = [f for f in arquivos if f.suffix in ['.crdownload', '.tmp']]
            if arquivos and not em_andamento:
                arquivo_recente = max(arquivos, key=os.path.getmtime)
                self.logger.info(f"Download concluído: {arquivo_recente.name}")
                return arquivo_recente
            time.sleep(1)
        self.logger.error("Timeout: Download não finalizou.")
        return None
    
    def _renomear_arquivo(self, arquivo_original, novo_nome_sem_extensao):
        if not arquivo_original or not arquivo_original.exists():
            return None
        
        try:
            # Descobre a extensão do arquivo
            extensao = arquivo_original.suffix
            
            # Cria o caminho final
            novo_arquivo = PASTA_DADOS / f"{novo_nome_sem_extensao}{extensao}"
            
            # Se já existir um arquivo com esse nome, remove 
            if novo_arquivo.exists():
                os.remove(novo_arquivo)
            
            # Renomeia
            arquivo_original.rename(novo_arquivo)
            self.logger.info(f"Arquivo renomeado para: {novo_arquivo.name}")
            return novo_arquivo
            
        except Exception as e:
            self.logger.error(f"Erro ao renomear arquivo: {e}")
            return arquivo_original
        
    # --- Extrair ---
    def extrair_relatorio(self):
        self.logger.info(f"--- Extraindo Arquivo ---")
        try:
            xpath_relatorio = '/html/body/nav/div/div/ul[1]/li[3]/a'
            
            botao_relatorio = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath_relatorio))
            )

            botao_relatorio.click()

            xpath_status = '//*[@id="navbarCollapse2"]/ul[1]/li[3]/ul/li[2]/a'
            
            botao_status = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath_status))
            )

            botao_status.click()

            self.logger.info("Tirando foto da tela antes de clicar...")
            self.driver.save_screenshot("debug_tela_invisivel.png")
            
            xpath_excel = '/html/body/div/form/div[2]/div[1]/button/span'
            
            botao_excel = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath_excel))
            )

            botao_excel.click()
            time.sleep(5)

            arquivo = self._aguardar_download()
            
            return self._renomear_arquivo(arquivo, "Sequenciamento CTB")
            
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return None
        
    def login(self):
        usuario = os.getenv('USER_LOGIN')
        password = os.getenv('USER_PASSWORD')
        self.logger.info(f'Realizando login')
        try:
            
            self.driver.get(URL_SITE)

            xpath_user = '//*[@id="matricula"]'
            
            campo_user = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath_user))
            )
            
            campo_user.clear() 
            campo_user.send_keys(usuario)

            xpath_password = '//*[@name="password"]'
            
            campo_password = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath_password))
            )
            campo_password.click()
            campo_password.clear() 
            campo_password.send_keys(password)

            xpath_enviar = '/html/body/div/div/div/form/button'

            campo_enviar = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath_enviar))
            )
            campo_enviar.click()
        except:
            ...