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
        """Cria um agente especializado em ler e compreender templates."""
        return Agent(
            role='Leitor de Template',
            goal='Ler e compreender o conteúdo completo do template fornecido',
            backstory="""Você é um especialista em análise de documentos técnicos, com vasta experiência
            em leitura e interpretação de templates de relatórios. Sua especialidade é extrair o máximo
            de informação possível do documento, compreendendo não apenas seu conteúdo, mas também sua
            finalidade e contexto. Você tem habilidade especial para identificar padrões, convenções e
            requisitos específicos em templates técnicos.""",
            llm=self.llm,
            verbose=False,
            allow_delegation=False,
        )

    def estruturador_template(self):
        return Agent(
            role='Analista de Estrutura de Documentos',
            goal='Identificar e extrair a estrutura hierárquica do template fornecido',
            backstory="""Você é um especialista em análise documental com vasta experiência em identificar 
            e mapear estruturas de documentos. Sua especialidade é compreender a hierarquia e organização 
            de documentos técnicos, especialmente relatórios geológicos.""",
            llm=self.llm,
            verbose=False,
            allow_delegation=False,
        )

    def identificador_secoes_incompletas(self):
        return Agent(
            role='Analista de Completude Documental',
            goal='Identificar seções que precisam ser preenchidas ou complementadas no template',
            backstory="""Você é um especialista em análise de qualidade documental, com foco em identificar 
            lacunas e pontos que precisam ser preenchidos em documentos técnicos. Sua especialidade é avaliar 
            a completude de cada seção e subseção, indicando claramente o que precisa ser adicionado ou 
            complementado.""",
            llm=self.llm,
            verbose=False,
            allow_delegation=False,
        )