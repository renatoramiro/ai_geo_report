from crewai import Crew
from .agents import Agents
from .tasks import Tasks
import os

class ReadTemplateCrew:
    def __init__(self):
        self.agents = Agents()
        self.tasks = Tasks()

    def run(self, file_path: str = None):
        if file_path is not None:
            relatorios_dir = os.path.join(os.getcwd(), 'relatorios')
            pdf_path = os.path.join(relatorios_dir, file_path)

            leitor = self.agents.leitor_template()
            identificar_template_task = self.tasks.identificar_template(leitor, pdf_path)

            crew = Crew(
                agents=[leitor],
                tasks=[identificar_template_task],
                verbose=True
            )
            result = crew.kickoff()
            return str(result.raw)
        else:
            return None

# def main():
#     """Função principal para executar a análise quando o script é rodado diretamente."""
#     crew = ReadTemplateCrew()
#     template_path = 'meu_template.pdf'
#     print(crew.run(file_path=template_path))

# if __name__ == "__main__":
#     main()