from crewai import Task
try:
    from tools.pdf_to_md_tool import PDFToMDTool
except ImportError:
    from .tools.pdf_to_md_tool import PDFToMDTool

class Tasks:
    def ler_template(self, agent, pdf_path: str):
        """Cria uma tarefa para ler e compreender o template."""
        return Task(
            agent=agent,
            description="""
Analise o template fornecido e forneça uma compreensão detalhada de seu conteúdo e propósito.

# INSTRUÇÕES
1. Converta o PDF para texto usando a ferramenta PDFToMDTool.
            """,
            expected_output="""
            O texto convertido pela ferramenta PDFToMDTool.
            """,
            tools=[PDFToMDTool(template_path=pdf_path)]
        )

    def identificar_estrutura(self, agent, pdf_path: str):
        return Task(
            agent=agent,
            description="""
OBJETIVO:
Extrair a estrutura hierárquica do template, usando apenas '#' para níveis.

INSTRUÇÕES:
1. Use a ferramenta PDFToMDTool para converter o PDF
2. Identifique todos os níveis do documento
3. Para cada nível use '#' da seguinte forma:
   - Nível 1: #
   - Nível 2: ##
   - Nível 3: ###
   - E assim por diante

REGRAS OBRIGATÓRIAS:
- NUNCA use três crases (```) em nenhum lugar da resposta
- NUNCA adicione a palavra 'markdown' ou 'md' na resposta
- NUNCA use qualquer formatação além dos '#'
- NUNCA adicione comentários ou observações
- NUNCA adicione linhas em branco extras
- NUNCA adicione texto além da estrutura
- Mantenha a numeração original das seções
- Preserve a hierarquia exata do documento

EXEMPLO DE RESPOSTA ESPERADA:
# Título do Relatório
## 1. Primeira Seção
### 1.1 Subseção
## 2. Segunda Seção
### 2.1 Subseção

LEMBRE-SE: Retorne APENAS a estrutura hierárquica, sem NENHUMA formatação adicional além dos '#'.
            """,
            expected_output="A estrutura hierárquica pura, usando apenas '#' para níveis.",
            tools=[PDFToMDTool(template_path=pdf_path)]
        )

    def identificar_secoes_incompletas(self, agent):
        return Task(
            agent=agent,
            description="""
Analise o resultado da tarefa anterior, que está em <content> e identifique as seções que precisam ser preenchidas.

<content>
{content}
</content>

# INSTRUÇÕES
1. Para cada seção, determine:
   - Se está vazia ou incompleta
   - Que tipo de informação é esperada
   - Quais dados precisam ser fornecidos

# FORMATO DA RESPOSTA
Liste cada seção que precisa ser preenchida com:
1. Caminho completo da seção (ex: "2.1 Endereço")
2. Status: [Vazio/Incompleto]
3. Informações necessárias: Lista objetiva do que precisa ser preenchido

# IMPORTANTE
* Seja específico e objetivo
* Use apenas fatos, não opiniões
* NÃO adicione comentários ou sugestões pessoais
* NÃO faça recomendações além do solicitado
* NÃO adicione conclusões ou observações finais
* Liste apenas as seções que realmente precisam de preenchimento
            """,
            expected_output="""
Lista objetiva de seções que precisam ser preenchidas, com status e informações necessárias.
            """
        )
