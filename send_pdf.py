from pathlib import Path
from send_whatsapp import SendWhatsapp

def send_all_pdfs(phone_number: str):
    """Envia todos os PDFs da pasta relatorios para um número específico."""
    whatsapp = SendWhatsapp()
    relatorios_dir = Path("/home/renato/projects/ai_geologia/relatorios")
    
    # Verificar se o diretório existe
    if not relatorios_dir.exists():
        print(f"Diretório não encontrado: {relatorios_dir}")
        return
    
    # Listar todos os PDFs no diretório
    pdfs = list(relatorios_dir.glob("*.pdf"))
    
    if not pdfs:
        print("Nenhum PDF encontrado no diretório")
        return
    
    print(f"Encontrados {len(pdfs)} PDFs para enviar")
    
    # Enviar cada PDF
    for pdf_path in pdfs:
        print(f"\nEnviando {pdf_path.name}...")
        whatsapp.PDF(
            number=phone_number,
            pdf_file=str(pdf_path),
            caption=f"Relatório Geológico: {pdf_path.stem}"
        )

if __name__ == "__main__":
    # Exemplo de uso
    PHONE_NUMBER = "558396369508"  # Substitua pelo número desejado
    try:
        send_all_pdfs(PHONE_NUMBER)
    except Exception as e:
        print(f"\nErro durante a execução: {str(e)}")
        raise
