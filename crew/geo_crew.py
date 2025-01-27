from crewai import Crew
from crew.agents import Agents
from crew.tasks import Tasks

class GeoCrew():
    def __init__(self):
        self.agents = Agents()
        self.tasks = Tasks()

    def run(self, user_data, file_name, write_style):
        coletor = self.agents.coletor_dados()
        relator = self.agents.escritor_relatorio()

        coletar_dados_task = self.tasks.coletar_dados(coletor)
        gerar_relatorio_task = self.tasks.gerar_relatorio(relator, file_name)

        crew = Crew(
            agents=[coletor, relator],
            tasks=[coletar_dados_task, gerar_relatorio_task],
            verbose=True
        )

        result = crew.kickoff(inputs={"user_data": user_data, "write_style": write_style})
        # print('========= Resultado ==========')
        # print(str(result.raw))
        return str(result.raw)

# lala = GeoCrew()
# lala.run(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))