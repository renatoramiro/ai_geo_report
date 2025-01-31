import os
import sys

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from crewai.flow.flow import Flow, listen, start, and_
from read_template_crew import EstruturadorCrew, IdentificadorSecoesCrew, LeitorTemplateCrew

class ReadTemplateFlow(Flow):

    @start()
    def start_method(self):
        return "Iniciando o fluxo de leitura de template"

    # @listen(start_method)
    # def ler_template(self):
    #     crew = LeitorTemplateCrew()
    #     template_path = 'meu_template.pdf'
    #     result = crew.run(file_path=template_path)
    #     self.state["leitura_template"] = result

    @listen(start_method)
    def obter_estrutura_do_template(self):
        crew = EstruturadorCrew()
        print('=== Estrutura do Template ===')
        template_path = 'meu_template.pdf'
        result = crew.run(file_path=template_path)
        self.state["estrutura_do_template"] = result
        print(self.state["estrutura_do_template"])
        print('============================')

    @listen(obter_estrutura_do_template)
    def identificar_pontos_incompletos(self):
        crew = IdentificadorSecoesCrew()
        result = crew.run(content=self.state["estrutura_do_template"] )
        self.state["pontos_incompletos"] = result

    @listen(identificar_pontos_incompletos)
    def finalizando(self):
        print('\n\n--- Finalizando o fluxo ---')
        print(self.state['estrutura_do_template'].replace('```', ''))
        print('------------------')
        print(self.state['pontos_incompletos'])

def main():
    """Função principal para executar a análise quando o script é rodado diretamente."""
    flow = ReadTemplateFlow()
    flow.kickoff()
    # flow.plot()

if __name__ == "__main__":
    main()