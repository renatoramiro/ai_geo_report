from crewai import Task
from .tools.generate_pdf_tool import GeneratePDFTool
from .tools.generate_docx_tool import GenerateDocxTool

class Tasks():
    def coletar_dados(self, agent):
        return Task(
            agent=agent,
            description="""
Mensagem do usuário: {user_data}
A partir da mensagem fornecida pelo usuário, estruture os dados com os seguintes pontos abaixo:
1. Identificação e localização: Nome do terreno, código de identificação, coordenadas geográficas, e localização detalhada (município, estado e país).
2. Objetivo do relatório: Por que esse terreno está sendo analisado (ex.: construção, análise ambiental, mineração)?
3. Características gerais do terreno:
    3.1 Área total do terreno
    3.2 Dimensões aproximadas
    3.3 Altitude média
    3.4 Descreva a topografia (plano, ondulado, acidentado, etc.)
    3.5 O uso atual do terreno
            """,
            expected_output="Informações detalhadas sobre o terreno"
        )

    def gerar_relatorio(self, agent, file_name):
        return Task(
            agent=agent,
            description="""
Com base nos dados fornecidos pelo agente Coletor de Dados e no estilo de escrita, que está em <write_style>, elabore um relatório geológico estruturado. O relatório deve incluir os seguintes tópicos:

1. Identificação e Localização: Nome ou código do terreno, coordenadas e localização detalhada.
2. Objetivo do Relatório: Descreva o motivo pelo qual o terreno está sendo analisado.
3. Características Gerais do Terreno: Inclua informações sobre topografia, área total, dimensões, altitude média, uso atual e histórico relevante.

Use linguagem clara, objetiva e profissional. Estruture o relatório com títulos e subtítulos para facilitar a leitura. Certifique-se de que todas as informações fornecidas sejam incorporadas corretamente.

Ao final do relatório, não inclua nenhuma consideração final ou informação, apenas inclua os dados fornecidos pelo agente Coletor de Dados.

<write_style>
{write_style}
</write_style>

Gere o relatório em PDF e Word.
            """,
            expected_output="Relatório geológico estruturado",
            tools=[
                GeneratePDFTool(file_name=file_name),
                GenerateDocxTool(word_file=file_name)
            ]
        )