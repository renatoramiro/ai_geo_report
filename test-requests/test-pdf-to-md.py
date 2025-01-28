import pymupdf4llm

md_text = pymupdf4llm.to_markdown("relatorios/template_relatorio.pdf")
print(md_text)