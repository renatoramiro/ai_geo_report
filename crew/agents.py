from crewai import Agent, LLM
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Agents():
    def __init__(self):
        self.llm = LLM(
            model="gpt-4o-mini",
            temperature=0.7,
        )

    def coletor_dados(self):
        return Agent(
            role = 'Coletor de Dados',
            goal = 'Reunir informações iniciais sobre um terreno para elaborar um relatório.',
            backstory='Você é um profissional experiente e especializado em coleta de dados de geologia.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def escritor_relatorio(self):
        return Agent(
            role = 'Escritor de Relatório',
            goal = 'Processar os dados fornecidos pelo Agente Coletor de Dados e elaborar um relatório geológico estruturado.',
            backstory='Vocé é um profissional experiente e especializado em gerar relatórios de geologia.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )