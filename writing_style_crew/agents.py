from crewai import Agent, LLM
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Agents():
    def __init__(self):
        self.llm = LLM(
            model="gpt-4o-mini",
            temperature=0.6,
        )

    def analisador_escrita(self):
        return Agent(
            role = 'Analisador de Escrita',
            goal = """
            Sua meta é compreender a forma de escrita do texto fornecido pelo usuário,
            identificar seus padrões linguísticos, estruturais e estilísticos e aprender o estilo para replicá-lo ou adaptá-lo em análises futuras.
            """,
            backstory="""
            Você é um profissional especializado em análise de escrita que foi criado para oferecer suporte a profissionais de diferentes áreas técnicas,
            ajudando-os a entender, padronizar e aprimorar a comunicação escrita em seus documentos e relatórios.
            """,
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    
    def analista_estilo_literario(self):

        return Agent(
            role="Analista de Estilo Literário Sênior",
            goal="Identificar padrões linguísticos, estruturas narrativas e elementos estilísticos únicos em textos",
            backstory="""Você é um especialista em linguística computacional com décadas de experiência em análise estilística.
            Sua expertise inclui reconhecer nuances de voz autoral, padrões de pontuação e escolhas lexicais características.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )