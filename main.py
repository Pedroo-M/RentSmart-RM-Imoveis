"""
Aplicação Principal do Sistema RentSmart — R.M Imóveis.

Responsável pela interação com o atendente/cliente via terminal, validação rigorosa
das entradas de dados, instanciação dos objetos de domínio e geração do orçamento
e da planilha CSV de projeção anual.
"""

from models import Apartamento, Casa, Estudio, Imovel
from orcamento import OrcamentoLocacao


class SistemaRentSmart:
    """Controlador principal da interface de atendimento do RentSmart."""

    @staticmethod
    def ler_opcao(mensagem: str, opcoes_validas: tuple[str, ...]) -> str:
        """Solicita uma opção textual até que o usuário informe um valor válido."""
        while True:
            entrada = input(mensagem).strip().upper()
            if entrada in opcoes_validas:
                return entrada
            print(f"[Erro] Opção inválida. Escolha entre: {', '.join(opcoes_validas)}.")

    @staticmethod
    def ler_sim_nao(mensagem: str) -> bool:
        """Solicita uma resposta binária (S/N) e retorna True para Sim e False para Não."""
        resposta = SistemaRentSmart.ler_opcao(mensagem, ("S", "N"))
        return resposta == "S"

    @staticmethod
    def ler_inteiro_intervalo(mensagem: str, minimo: int, maximo: int | None = None) -> int:
        """Solicita um número inteiro validado dentro de um intervalo permitido."""
        while True:
            entrada = input(mensagem).strip()
            if not entrada.isdigit():
                print("[Erro] Digite apenas números inteiros válidos.")
                continue
            valor = int(entrada)
            if valor < minimo:
                print(f"[Erro] O valor mínimo permitido é {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"[Erro] O valor máximo permitido é {maximo}.")
                continue
            return valor

    def construir_imovel(self) -> Imovel:
        """Coleta os dados do imóvel escolhido e instancia a subclasse correspondente."""
        print("\nSelecione a categoria do imóvel:")
        print("  [1] Apartamento (Base: R$ 700,00)")
        print("  [2] Casa        (Base: R$ 900,00)")
        print("  [3] Estúdio     (Base: R$ 1.200,00)")

        categoria = self.ler_opcao("Digite a opção desejada (1, 2 ou 3): ", ("1", "2", "3"))

        if categoria == "1":
            quartos = self.ler_inteiro_intervalo(
                "Quantidade de quartos (1 ou 2): ", minimo=1, maximo=2
            )
            garagem = self.ler_sim_nao("Deseja incluir vaga de garagem (+R$ 300,00)? [S/N]: ")
            criancas = self.ler_sim_nao(
                "O locatário possui crianças residindo no imóvel? [S/N]: "
            )
            return Apartamento(
                quartos=quartos,
                possui_garagem=garagem,
                possui_criancas=criancas,
            )

        if categoria == "2":
            quartos = self.ler_inteiro_intervalo(
                "Quantidade de quartos (1 ou 2): ", minimo=1, maximo=2
            )
            garagem = self.ler_sim_nao("Deseja incluir vaga de garagem (+R$ 300,00)? [S/N]: ")
            return Casa(quartos=quartos, possui_garagem=garagem)

        # Categoria "3": Estúdio
        incluir_pacote = self.ler_sim_nao(
            "Deseja contratar o pacote inicial de 2 vagas de estacionamento (+R$ 250,00)? [S/N]: "
        )
        vagas_adicionais = 0
        if incluir_pacote:
            vagas_adicionais = self.ler_inteiro_intervalo(
                "Quantas vagas adicionais deseja incluir (R$ 60,00 cada)? [0 ou mais]: ",
                minimo=0,
            )
        return Estudio(
            incluir_pacote_vagas=incluir_pacote,
            vagas_adicionais=vagas_adicionais,
        )

    def executar(self) -> None:
        """Executa o fluxo principal do sistema RentSmart."""
        print("=" * 64)
        print("       BEM-VINDO AO RENTSMART — SISTEMA R.M IMÓVEIS")
        print("=" * 64)

        while True:
            imovel = self.construir_imovel()
            parcelas = self.ler_inteiro_intervalo(
                "Em quantas parcelas deseja pagar a taxa contratual de R$ 2.000,00 (1 a 5)? ",
                minimo=1,
                maximo=5,
            )

            orcamento = OrcamentoLocacao(imovel=imovel, parcelas_taxa=parcelas)
            print("\n" + orcamento.gerar_resumo_formatado())

            nome_arquivo = f"orcamento_{imovel.categoria.lower().replace('ú', 'u')}_12_meses.csv"
            caminho_salvo = orcamento.exportar_csv(nome_arquivo)
            print(f"\n[OK] Projeção de 12 meses exportada com sucesso para: {caminho_salvo}")

            if not self.ler_sim_nao("\nDeseja realizar um novo orçamento? [S/N]: "):
                print("\nEncerrando o RentSmart. Obrigado por utilizar o sistema da R.M Imóveis!")
                break


if __name__ == "__main__":
    sistema = SistemaRentSmart()
    sistema.executar()
