from crewai import Agent, LLM
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Agents:
    def __init__(self):
        self.llm = LLM(
            model="gpt-4o-mini",
            temperature=0.7,
        )

    def leitor_template(self):
        return Agent(
            role="Leitor de Template",
            goal="Identificar e interpretar o conteúdo estruturado de um template de relatório.",
            backstory="""Você é um especialista em analise de documentos e tem habilidades para identificar e 
            interpretar estruturas de dados e elementos visuais de um template de relatório.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )