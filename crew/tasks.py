from crewai import Task
from .tools.generate_pdf_tool import GeneratePDFTool
from .tools.generate_docx_tool import GenerateDocxTool

class Tasks():
    def coletar_dados(self, agent):
        return Task(
            agent=agent,
            description="""
Analise os dados fornecidos pelo usuário em <user_data> e colete todas as informações relevantes para um relatório geológico, seguindo a estrutura de tópicos fornecida em <topicos>.

<user_data>
{user_data}
</user_data>

<topicos>
{topics}
</topicos>

# IMPORTANTE
* Extraia APENAS as informações que se encaixam nos tópicos fornecidos.
* NÃO adicione informações extras ou suposições.
* NÃO inclua o texto "<topicos>" ou "</topicos>" na sua resposta.
* NÃO inclua o texto "{topics}" na sua resposta.
* Organize as informações seguindo EXATAMENTE a estrutura dos tópicos fornecidos.
* Se alguma informação estiver faltando, indique claramente com "[Informação não fornecida]".
            """,
            expected_output="""
Dados coletados e organizados de acordo com os tópicos do relatório.
            """
        )

    def gerar_relatorio(self, agent, file_name):
        return Task(
            agent=agent,
            description="""
Você é um geólogo experiente com excelente capacidade de escrita. Usando sua criatividade e conhecimento técnico, elabore um relatório geológico estruturado baseado nos dados fornecidos pelo agente Coletor de Dados.

O relatório deve seguir RIGOROSAMENTE o estilo de escrita definido em <write_style>. Adapte sua linguagem e tom para corresponder exatamente ao estilo solicitado pelo usuário.

<write_style>
{write_style}
</write_style>

O relatório deve incluir os tópicos que estão em <topicos>:

<topicos>
{topics}
</topicos>

# DIRETRIZES DE ESCRITA
* Use sua criatividade para elaborar descrições vívidas e detalhadas, mantendo a precisão técnica.
* Adapte o tom e vocabulário para corresponder ao estilo de escrita solicitado.
* Desenvolva cada tópico de forma completa e envolvente.
* Mantenha uma narrativa coesa e fluida entre as seções.
* Use linguagem técnica apropriada, mas mantenha a clareza conforme o estilo solicitado.

# IMPORTANTE
* NÃO adicione considerações finais ou informações extras no final do relatório.
* NÃO inclua o texto "<topicos>" ou "</topicos>" no relatório final.
* NÃO inclua o texto "{topics}" no relatório final.
* Siga EXATAMENTE a estrutura dos tópicos fornecidos.
* Mantenha o relatório conciso e direto ao ponto.
* NÃO adicione seções ou tópicos que não foram solicitados.
* SEMPRE inclua todas as informações fornecidas pelo agente Coletor de Dados.
* Crie um título principal baseado nas informações do relatório.
* Mantenha a numeração exata das seções e subseções conforme fornecida em <topicos>.

Gere o relatório em PDF e Word.
            """,
            expected_output="Relatório geológico estruturado com estilo personalizado",
            tools=[
                GeneratePDFTool(file_name=file_name),
                GenerateDocxTool(word_file=file_name)
            ]
        )