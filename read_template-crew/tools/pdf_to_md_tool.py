from crewai.tools import BaseTool
import pymupdf4llm

class PDFToMDTool(BaseTool):
    name: str = "PDFToMD"
    description: str = "Convert PDF to Markdown"
    template_path: str

    def _run(self, template_path: str) -> str:
        return pymupdf4llm.to_markdown(self.template_path)