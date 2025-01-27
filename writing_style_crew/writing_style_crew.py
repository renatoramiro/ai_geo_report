from crewai import Crew
from writing_style_crew.agents import Agents
from writing_style_crew.tasks import Tasks
import os

class WritingStyleCrew():
    def __init__(self):
        self.agents = Agents()
        self.tasks = Tasks()

    def run(self, pdf_path: str = None):
        """
        Executa a análise de estilo de escrita em um arquivo PDF.
        
        Args:
            pdf_path (str, optional): Caminho para o arquivo PDF. Se não fornecido,
                                    será usado um arquivo padrão.
        """
        analista = self.agents.analisador_escrita()

        # Usar os.path.join para criar o caminho do arquivo
        if pdf_path is None:
            pdf_path = os.path.join('relatorios', 'PCA_RCA_Processo_Pedras_Fogo.pdf')

        analise_de_escrita_task = self.tasks.analisar_escrita2(analista, pdf_path)

        crew = Crew(
            agents=[analista],
            tasks=[analise_de_escrita_task],
            verbose=True
        )

        result = crew.kickoff()
        # print('========= Resultado ==========')
        # print(str(result.raw))
        return str(result.raw)

# def main():
#     """Função principal para executar a análise quando o script é rodado diretamente."""
#     crew = WritingStyleCrew()
#     crew.run()

# if __name__ == "__main__":
#     main()
