import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RAIZ_PROJETO = Path(__file__).parent.parent.resolve()

PASTA_DADOS = RAIZ_PROJETO / "relatorios"
PASTA_LOGS = RAIZ_PROJETO / "logs"

for pasta in [PASTA_DADOS, PASTA_LOGS]:
    pasta.mkdir(parents=True, exist_ok=True)

URL_SITE = os.getenv("URL_SITE") 
HEADLESS = True  # False = Ver o navegador abrindo | True = Rodar escondido
TIMEOUT_PADRAO = 20