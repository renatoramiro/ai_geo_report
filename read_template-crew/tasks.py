from crewai import Task
from tools.pdf_to_md_tool import PDFToMDTool

class Tasks:
    def identificar_template(self, agent, pdf_path: str):
        return Task(
            agent=agent,
            tools=[
                PDFToMDTool(template_path=pdf_path)
            ],
            description="""
Seu objetivo é identificar a estrutura do texto fornecido pelo usuário e destacar os pontos que precisam ser preenchidos.
Siga as instruções em <instrucoes>:

<instrucoes>
* Leia o texto fornecido pelo usuário através da ferramenta PDFToMD.
* Analise a estrutura do documento, identificando os títulos, subtítulos e seções presentes.
* Identifique as partes do documento que aparentam estar incompletas ou não possuem informações suficientes. Considere áreas em branco ou ausência de conteúdo após os títulos e subtítulos.
* Formule uma saída clara e organizada, apontando a estrutura do documento e destacando as seções que parecem estar incompletas ou que precisam de informações adicionais.
</instrucoes>
            """,
            expected_output="""
            Lista os tópicos do documento.
            Identifica as seções que precisam ser preenchidas e as destaca para o usuário.
            """
        )
