# 🤖 RPA - Automação de Extração de Relatórios

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-green?style=for-the-badge&logo=selenium)
![Agendamento](https://img.shields.io/badge/Status-Automatizado-success?style=for-the-badge)

## 📌 Sobre o Projeto
Este projeto é um **Robô de Automação de Processos (RPA)** desenvolvido em Python. O objetivo principal é eliminar o trabalho manual de login, navegação e extração de dados em um sistema web corporativo, baixando os relatórios essenciais que alimentam a inteligência de negócios (Power BI) da empresa.

O robô opera de forma autônoma (headless/background), aguarda a conclusão segura de downloads e possui um sistema de agendamento inteligente baseado em horário comercial.

## 🚀 Funcionalidades Principais
* **Login Automatizado:** Mapeamento de DOM seguro e injeção de credenciais via variáveis de ambiente.
* **Download Silencioso:** Configuração de `ChromeOptions` para direcionar downloads automaticamente para a pasta de dados (`PASTA_DADOS`), sem pop-ups do Windows.
* **Validação de Arquivo:** Algoritmo que monitora a pasta de destino e aguarda a conversão do arquivo temporário (`.crdownload`) para o arquivo final.
* **Agendamento Inteligente:** Utiliza a biblioteca `schedule` para rodar em intervalos programados, com validação de horário comercial (após as 06:00h).
* **Tratamento de Erros:** Estrutura robusta de `try/except/finally` garantindo que o ciclo de vida do WebDriver seja encerrado corretamente, evitando vazamento de memória (processos zumbis).

## 🛠️ Tecnologias Utilizadas
* **[Python](https://www.python.org/)** - Linguagem principal.
* **[Selenium WebDriver](https://www.selenium.dev/)** - Para automação e interação com o navegador.
* **[python-dotenv](https://pypi.org/project/python-dotenv/)** - Gerenciamento de credenciais e segurança da informação.
* **[schedule](https://pypi.org/project/schedule/)** - Orquestração e agendamento de tarefas.

## ⚙️ Como Configurar e Rodar o Projeto

### 1. Pré-requisitos
* Python 3.x instalado na máquina.
* Google Chrome instalado.
* Arquivo `chromedriver.exe` compatível com a versão do seu Chrome (coloque-o na raiz do projeto).

### 2. Instalação
Clone o repositório e crie um ambiente virtual para não gerar conflito com outras bibliotecas da sua máquina:

```bash
# Criação do ambiente virtual
python -m venv venv

# Ativação do ambiente (Windows)
venv\Scripts\activate

# Instalação das dependências
pip install -r requirements.txt
