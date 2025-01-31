from crewai.tools import BaseTool
import pymupdf4llm

class PDFToMDTool(BaseTool):
    name: str = "PDFToMD"
    description: str = "Convert PDF to Markdown"
    template_path: str

    def _run(self) -> str:
        """Converte o arquivo PDF para Markdown."""
        return pymupdf4llm.to_markdown(self.template_path)