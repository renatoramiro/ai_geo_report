from crewai import Crew
try:
    from agents import Agents
    from tasks import Tasks
except ImportError:
    from .agents import Agents
    from .tasks import Tasks
import os

class LeitorTemplateCrew:
    """Crew responsável pela leitura inicial e compreensão do template."""
    
    def __init__(self):
        self.agents = Agents()
        self.tasks = Tasks()
    
    def run(self, file_path: str = None):
        """Executa a leitura e análise inicial do template."""
        if file_path is None:
            return None
            
        relatorios_dir = os.path.join(os.getcwd(), 'relatorios')
        pdf_path = os.path.join(relatorios_dir, file_path)
        
        leitor = self.agents.leitor_template()
        crew = Crew(
            agents=[leitor],
            tasks=[self.tasks.ler_template(leitor, pdf_path)],
            verbose=True
        )
        
        result = crew.kickoff()
        return str(result)


class EstruturadorCrew:
    """Crew responsável por identificar a estrutura do template."""
    
    def __init__(self):
        self.agents = Agents()
        self.tasks = Tasks()
    
    def run(self, file_path: str = None):
        """Executa a análise da estrutura do template."""
        if file_path is None:
            return None
        
        relatorios_dir = os.path.join(os.getcwd(), 'relatorios')
        pdf_path = os.path.join(relatorios_dir, file_path)
        
        estruturador = self.agents.estruturador_template()
        crew = Crew(
            agents=[estruturador],
            tasks=[self.tasks.identificar_estrutura(estruturador, pdf_path)],
            verbose=True
        )
        
        result = crew.kickoff()
        return str(result)


class IdentificadorSecoesCrew:
    """Crew responsável por identificar seções incompletas do template."""
    
    def __init__(self):
        self.agents = Agents()
        self.tasks = Tasks()
    
    def run(self, content: str = None):
        """
        Executa a análise das seções incompletas.
        
        Args:
            content: Conteúdo do template em string
        """
        if content is None:
            return None
            
        identificador = self.agents.identificador_secoes_incompletas()
        crew = Crew(
            agents=[identificador],
            tasks=[self.tasks.identificar_secoes_incompletas(identificador)],
            verbose=True
        )
        
        result = crew.kickoff(inputs={"content": content})
        return str(result)


# Exemplo de uso:
def main():
    """Função principal para executar a análise quando o script é rodado diretamente."""
    template_path = 'meu_template.pdf'

    leitor = LeitorTemplateCrew()
    leitura_result = leitor.run(template_path)
    print("=== Leitura do Template ===")
    print(leitura_result)
    
    # Primeiro, analisa a estrutura
    estruturador = EstruturadorCrew()
    estrutura_result = estruturador.run(leitura_result)
    
    # Depois, identifica seções incompletas
    identificador = IdentificadorSecoesCrew()
    secoes_result = identificador.run(leitura_result)
    
    print("=== Estrutura do Template ===")
    print(estrutura_result)
    print("\n=== Seções Incompletas ===")
    print(secoes_result)

if __name__ == "__main__":
    main()