from crewai import Task
from crewai_tools import PDFSearchTool

class Tasks:
    def analisar_escrita(self, agent, pdf_path: str):
        return Task(
            agent=agent,
            description="""
            Analise o texto fornecido pelo usuário, extraindo informações sobre seu estilo de escrita e aprendendo os padrões principais. A análise deve abranger:

Padrões de Escrita:

1. Vocabulário: Identificação de termos técnicos, jargões específicos da área e linguagem acessível ou especializada.
* Estrutura: Organização do texto (seções, parágrafos, uso de subtítulos).
* Estilo: Predominância técnica, descritiva, analítica, narrativa ou persuasiva.

2.Características Gerais:

* Tom: Formal, neutro, objetivo ou persuasivo.
* Complexidade: Frases diretas ou elaboradas.
* Propósito: Informar, descrever, analisar, persuadir ou explicar.
            """,
            expected_output="""
            * Identificação clara do estilo predominante e suas combinações, se houver.
* Caracterização detalhada do vocabulário, tom e estrutura textual.
* Resumo do aprendizado, destacando os elementos-chave do texto e sugestões sobre como replicar o estilo identificado.

Exemplo de Output:
Texto: "O inventário florístico revelou a predominância de espécies arbóreas adaptadas a solos argilosos e bem drenados. Dados de biodiversidade sugerem alta resiliência ecológica frente a mudanças climáticas."

Resposta:

Estilo Identificado: Técnico e descritivo.
Características principais:
Vocabulário: Uso de termos técnicos como "inventário florístico", "resiliência ecológica" e "solos argilosos".
Estrutura: Descrição clara de resultados seguida de análise técnica.
Tom: Objetivo e formal.

Resumo do aprendizado: O texto apresenta uma linguagem técnica com foco descritivo e analítico, utilizando termos específicos para comunicar dados ecológicos de forma clara e objetiva.
            """,
            tools=[
                PDFSearchTool(pdf=pdf_path)
            ]
        )

    def analisar_escrita2(self, agent, pdf_path: str):
        return Task(
            agent=agent,
            tools=[
                PDFSearchTool(pdf=pdf_path)
            ],
            description="""
            Analise o texto fornecido pelo usuário e identifique as características principais do estilo de escrita. Certifique-se de incluir **exemplos diretos** retirados do próprio texto para cada ponto de análise. A análise deve abranger:  
            1. **Estilo Predominante:** Identifique se o texto é técnico, descritivo, analítico, narrativo ou persuasivo (ou uma combinação desses) e inclua um exemplo retirado do texto que justifique sua classificação.  
            2. **Tom:** Determine se o texto é formal, neutro, objetivo ou persuasivo e inclua um exemplo que demonstre o tom identificado.  
            3. **Vocabulário:** Avalie se o vocabulário é especializado, técnico, acessível ou geral, **sempre exemplificando** com palavras ou frases retiradas do texto.  
            4. **Estrutura:** Indique se o texto é bem organizado, segmentado ou fluido, **fornecendo um exemplo que evidencie essa característica**. 
            """,
            expected_output="""
            Responda apenas com as análises e exemplos diretos retirados do texto do usuário para justificar sua avaliação. Certifique-se de fornecer exemplos para **todos os pontos**, e, se não encontrar exemplos claros, explique por que não foi possível identificar.  

            Exemplo de Output:  
            - **Estilo:** Técnico e descritivo. Exemplo: "O perfil do solo apresenta uma camada superficial rica em матéria orgânica, seguida por camadas de argila compactada."  
            - **Tom:** Formal e objetivo. Exemplo: "Os dados coletados indicam uma correlação direta entre a densidade do solo e sua capacidade de retenção hídrica."  
            - **Vocabulário:** Especializado e técnico. Exemplo: "Termos como 'matéria orgânica' e 'retenção hídrica' demonstram o uso de linguagem técnica."  
            - **Estrutura:** Bem organizado e segmentado. Exemplo: "O texto apresenta as seções 'Introdução', 'Metodologia' e 'Resultados', indicando uma organização lógica." 
            """
        )

    def analise_de_escrita(self, agent, pdf_path: str):
        return Task(
            description="""Analise o texto extraído do PDF fornecido para identificar:
            1. Tom predominante (formal, coloquial, técnico)
            2. Estrutura de parágrafos e frases
            3. Uso de recursos retóricos (metáforas, aliterações)
            4. Padrões de vocabulário e repetição lexical
            5. Estilo de pontuação característico""",
            expected_output="""Um relatório estruturado em JSON contendo:
            - Categorização do estilo (ex: acadêmico, jornalístico, criativo)
            - Lista de características identificadas com exemplos textuais
            - Análise quantitativa (taxa de complexidade lexical, densidade de metáforas)
            - Recomendações para replicação do estilo""",
            agent=agent,
            tools=[
                PDFSearchTool(pdf=pdf_path)
            ]
        )