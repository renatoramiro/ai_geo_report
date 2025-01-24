import os
from crewai.tools import BaseTool
from md2pdf.core import md2pdf

class GeneratePDFTool(BaseTool):
    name: str = "GeneratePDF"
    description: str = "Gera um PDF a partir de um Markdown."
    file_name: str

    def _run(self, markdown: str) -> str:
        try:
            # Criar diretório de relatórios se não existir
            relatorios_dir = os.path.join(os.getcwd(), 'relatorios')
            # relatorios_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "relatorios")
            os.makedirs(relatorios_dir, exist_ok=True)
            
            # Gerar PDF usando caminho relativo
            pdf_name = os.path.join(relatorios_dir, f'{self.file_name}.pdf')
            
            md2pdf(pdf_file_path=pdf_name, md_content=markdown)
            
            return pdf_name
        except Exception as e:
            raise e

    async def _arun(self, markdown: str) -> str:
        raise NotImplementedError("GeneratePDFTool não suporta execução assíncrona")