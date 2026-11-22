"""
RentSmart — Sistema de Orçamento de Locação com Python e Orientação a Objetos
Cliente: R.M Imóveis

Arquivo único consolidado contendo:
1. Modelos de Domínio (Imovel, Apartamento, Casa, Estudio)
2. Cálculo de Orçamento e Exportação CSV (OrcamentoLocacao)
3. Interface de Atendimento e Validação de Entradas (SistemaRentSmart)
4. Bateria Automatizada de Testes (executar via: python rentsmart.py --testar)
"""

from abc import ABC, abstractmethod
import csv
import sys


# ==============================================================================
# 1. MODELOS DE DOMÍNIO (ABSTRAÇÃO, ENCAPSULAMENTO, HERANÇA E POLIMORFISMO)
# ==============================================================================


class Imovel(ABC):
    """Classe base abstrata que representa um imóvel disponível para locação."""

    TAXA_CONTRATUAL_PADRAO: float = 2000.00

    def __init__(self, categoria: str, valor_base: float) -> None:
        if valor_base <= 0:
            raise ValueError("O valor-base do imóvel deve ser maior que zero.")
        self._categoria: str = categoria
        self._valor_base: float = float(valor_base)
        self._taxa_contratual: float = self.TAXA_CONTRATUAL_PADRAO

    @property
    def categoria(self) -> str:
        """Retorna a categoria do imóvel (Apartamento, Casa ou Estúdio)."""
        return self._categoria

    @property
    def valor_base(self) -> float:
        """Retorna o valor-base mensal do imóvel."""
        return self._valor_base

    @property
    def taxa_contratual(self) -> float:
        """Retorna o valor total da taxa contratual da imobiliária."""
        return self._taxa_contratual

    @abstractmethod
    def calcular_adicionais(self) -> float:
        """Calcula a soma dos valores adicionais específicos do imóvel."""

    def calcular_desconto(self, subtotal: float) -> float:
        """Calcula o desconto aplicável sobre o subtotal (base + adicionais).

        Por padrão, imóveis não possuem desconto comercial (retorna 0.0).
        Subclasses com regras promocionais sobrescrevem este método.
        """
        return 0.0

    def calcular_aluguel_mensal(self) -> float:
        """Calcula o valor final do aluguel mensal (base + adicionais - desconto)."""
        subtotal = self._valor_base + self.calcular_adicionais()
        desconto = self.calcular_desconto(subtotal)
        return round(subtotal - desconto, 2)

    @abstractmethod
    def obter_itens_composicao(self) -> list[tuple[str, float]]:
        """Retorna a lista detalhada de itens que compõem o aluguel mensal."""


class Apartamento(Imovel):
    """Representa um apartamento para locação na R.M Imóveis."""

    VALOR_BASE_1_QUARTO: float = 700.00
    ADICIONAL_2_QUARTOS: float = 200.00
    ADICIONAL_GARAGEM: float = 300.00
    PERCENTUAL_DESCONTO_SEM_CRIANCAS: float = 0.05

    def __init__(
        self,
        quartos: int = 1,
        possui_garagem: bool = False,
        possui_criancas: bool = True,
    ) -> None:
        super().__init__(categoria="Apartamento", valor_base=self.VALOR_BASE_1_QUARTO)
        if quartos not in (1, 2):
            raise ValueError("Apartamentos devem possuir 1 ou 2 quartos.")
        self._quartos: int = quartos
        self._possui_garagem: bool = bool(possui_garagem)
        self._possui_criancas: bool = bool(possui_criancas)

    @property
    def quartos(self) -> int:
        return self._quartos

    @property
    def possui_garagem(self) -> bool:
        return self._possui_garagem

    @property
    def possui_criancas(self) -> bool:
        return self._possui_criancas

    def calcular_adicionais(self) -> float:
        adicional = 0.0
        if self._quartos == 2:
            adicional += self.ADICIONAL_2_QUARTOS
        if self._possui_garagem:
            adicional += self.ADICIONAL_GARAGEM
        return round(adicional, 2)

    def calcular_desconto(self, subtotal: float) -> float:
        if not self._possui_criancas:
            return round(subtotal * self.PERCENTUAL_DESCONTO_SEM_CRIANCAS, 2)
        return 0.0

    def obter_itens_composicao(self) -> list[tuple[str, float]]:
        itens: list[tuple[str, float]] = [
            ("Aluguel-base (Apartamento 1 quarto)", self._valor_base)
        ]
        if self._quartos == 2:
            itens.append(("Adicional 2º quarto", self.ADICIONAL_2_QUARTOS))
        if self._possui_garagem:
            itens.append(("Adicional vaga de garagem", self.ADICIONAL_GARAGEM))

        subtotal = self._valor_base + self.calcular_adicionais()
        desconto = self.calcular_desconto(subtotal)
        if desconto > 0:
            itens.append(("Desconto comercial (5% - sem crianças)", -desconto))
        return itens


class Casa(Imovel):
    """Representa uma casa para locação na R.M Imóveis."""

    VALOR_BASE_1_QUARTO: float = 900.00
    ADICIONAL_2_QUARTOS: float = 250.00
    ADICIONAL_GARAGEM: float = 300.00

    def __init__(self, quartos: int = 1, possui_garagem: bool = False) -> None:
        super().__init__(categoria="Casa", valor_base=self.VALOR_BASE_1_QUARTO)
        if quartos not in (1, 2):
            raise ValueError("Casas devem possuir 1 ou 2 quartos.")
        self._quartos: int = quartos
        self._possui_garagem: bool = bool(possui_garagem)

    @property
    def quartos(self) -> int:
        return self._quartos

    @property
    def possui_garagem(self) -> bool:
        return self._possui_garagem

    def calcular_adicionais(self) -> float:
        adicional = 0.0
        if self._quartos == 2:
            adicional += self.ADICIONAL_2_QUARTOS
        if self._possui_garagem:
            adicional += self.ADICIONAL_GARAGEM
        return round(adicional, 2)

    def obter_itens_composicao(self) -> list[tuple[str, float]]:
        itens: list[tuple[str, float]] = [
            ("Aluguel-base (Casa 1 quarto)", self._valor_base)
        ]
        if self._quartos == 2:
            itens.append(("Adicional 2º quarto", self.ADICIONAL_2_QUARTOS))
        if self._possui_garagem:
            itens.append(("Adicional vaga de garagem", self.ADICIONAL_GARAGEM))
        return itens


class Estudio(Imovel):
    """Representa um estúdio para locação na R.M Imóveis."""

    VALOR_BASE: float = 1200.00
    PACOTE_INICIAL_2_VAGAS: float = 250.00
    VALOR_VAGA_ADICIONAL: float = 60.00

    def __init__(
        self,
        incluir_pacote_vagas: bool = False,
        vagas_adicionais: int = 0,
    ) -> None:
        super().__init__(categoria="Estúdio", valor_base=self.VALOR_BASE)
        if vagas_adicionais < 0:
            raise ValueError("A quantidade de vagas adicionais não pode ser negativa.")
        if not incluir_pacote_vagas and vagas_adicionais > 0:
            raise ValueError(
                "Para contratar vagas adicionais, é necessário incluir o pacote inicial de 2 vagas."
            )
        self._incluir_pacote_vagas: bool = bool(incluir_pacote_vagas)
        self._vagas_adicionais: int = int(vagas_adicionais)

    @property
    def incluir_pacote_vagas(self) -> bool:
        return self._incluir_pacote_vagas

    @property
    def vagas_adicionais(self) -> int:
        return self._vagas_adicionais

    @property
    def total_vagas(self) -> int:
        if not self._incluir_pacote_vagas:
            return 0
        return 2 + self._vagas_adicionais

    def calcular_adicionais(self) -> float:
        if not self._incluir_pacote_vagas:
            return 0.0
        adicional = self.PACOTE_INICIAL_2_VAGAS + (
            self._vagas_adicionais * self.VALOR_VAGA_ADICIONAL
        )
        return round(adicional, 2)

    def obter_itens_composicao(self) -> list[tuple[str, float]]:
        itens: list[tuple[str, float]] = [
            ("Aluguel-base (Estúdio)", self._valor_base)
        ]
        if self._incluir_pacote_vagas:
            itens.append(
                ("Pacote inicial de estacionamento (2 vagas)", self.PACOTE_INICIAL_2_VAGAS)
            )
            if self._vagas_adicionais > 0:
                valor_extras = round(
                    self._vagas_adicionais * self.VALOR_VAGA_ADICIONAL, 2
                )
                itens.append(
                    (
                        f"Vagas adicionais ({self._vagas_adicionais}x R$ 60,00)",
                        valor_extras,
                    )
                )
        return itens


# ==============================================================================
# 2. ORÇAMENTO E PROJEÇÃO FINANCEIRA (DEMONSTRATIVO E EXPORTAÇÃO CSV)
# ==============================================================================


def formatar_moeda(valor: float) -> str:
    """Formata um valor numérico no padrão monetário brasileiro (R$ X.XXX,XX)."""
    sinal = "-" if valor < 0 else ""
    valor_abs = abs(valor)
    texto = f"{valor_abs:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{sinal}R$ {texto}"


class OrcamentoLocacao:
    """Gerencia o cálculo, a apresentação e a exportação CSV de um orçamento de locação."""

    MIN_PARCELAS: int = 1
    MAX_PARCELAS: int = 5
    MESES_PROJECAO: int = 12

    def __init__(self, imovel: Imovel, parcelas_taxa: int = 1) -> None:
        if not isinstance(imovel, Imovel):
            raise TypeError("O orçamento exige uma instância válida de Imovel.")
        if not (self.MIN_PARCELAS <= parcelas_taxa <= self.MAX_PARCELAS):
            raise ValueError(
                f"O parcelamento da taxa contratual deve estar entre "
                f"{self.MIN_PARCELAS} e {self.MAX_PARCELAS} parcelas."
            )
        self._imovel: Imovel = imovel
        self._parcelas_taxa: int = int(parcelas_taxa)

    @property
    def imovel(self) -> Imovel:
        return self._imovel

    @property
    def parcelas_taxa(self) -> int:
        return self._parcelas_taxa

    def calcular_valor_parcela_taxa(self) -> float:
        """Calcula o valor individual de cada parcela da taxa contratual."""
        return round(self._imovel.taxa_contratual / self._parcelas_taxa, 2)

    def gerar_projecao_12_meses(self) -> list[dict[str, str | int | float]]:
        """Gera a projeção mês a mês (Meses 1 a 12) do primeiro ano de locação."""
        aluguel_mensal = self._imovel.calcular_aluguel_mensal()
        valor_parcela = self.calcular_valor_parcela_taxa()
        projecao: list[dict[str, str | int | float]] = []

        for mes in range(1, self.MESES_PROJECAO + 1):
            if mes <= self._parcelas_taxa:
                taxa_no_mes = valor_parcela
                status_taxa = f"Parcela {mes}/{self._parcelas_taxa}"
            else:
                taxa_no_mes = 0.00
                status_taxa = "Quitada"

            total_mes = round(aluguel_mensal + taxa_no_mes, 2)
            projecao.append(
                {
                    "Mes": mes,
                    "Categoria_Imovel": self._imovel.categoria,
                    "Aluguel_Mensal": aluguel_mensal,
                    "Parcela_Taxa_Contratual": taxa_no_mes,
                    "Status_Taxa_Contratual": status_taxa,
                    "Total_Previsto_Mes": total_mes,
                }
            )
        return projecao

    def gerar_resumo_formatado(self) -> str:
        """Constrói o demonstrativo detalhado separando aluguel mensal e taxa contratual."""
        aluguel_mensal = self._imovel.calcular_aluguel_mensal()
        valor_parcela = self.calcular_valor_parcela_taxa()
        total_anual_aluguel = round(aluguel_mensal * self.MESES_PROJECAO, 2)
        total_primeiro_ano = round(total_anual_aluguel + self._imovel.taxa_contratual, 2)

        linhas = [
            "=" * 64,
            "        ORÇAMENTO DE LOCAÇÃO — R.M IMÓVEIS (RENTSMART)",
            "=" * 64,
            f"Categoria do Imóvel : {self._imovel.categoria}",
            "-" * 64,
            "1. COMPOSIÇÃO DO ALUGUEL MENSAL:",
        ]

        for descricao, valor in self._imovel.obter_itens_composicao():
            linhas.append(f"   - {descricao:<43} {formatar_moeda(valor):>13}")

        linhas.extend(
            [
                "-" * 64,
                f"   VALOR FINAL DO ALUGUEL MENSAL:              {formatar_moeda(aluguel_mensal):>13}",
                "=" * 64,
                "2. TAXA CONTRATUAL (COBRANÇA SEPARADA DO ALUGUEL):",
                f"   - Valor Total da Taxa Contratual:           {formatar_moeda(self._imovel.taxa_contratual):>13}",
                f"   - Condição de Pagamento Escolhida:          {self._parcelas_taxa}x de {formatar_moeda(valor_parcela)}",
                "-" * 64,
                "3. RESUMO FINANCEIRO DO PRIMEIRO ANO (12 MESES):",
                f"   - Meses 1 a {self._parcelas_taxa} (Aluguel + Parcela da Taxa):  "
                f"{formatar_moeda(aluguel_mensal + valor_parcela):>13}/mês",
            ]
        )

        if self._parcelas_taxa < self.MESES_PROJECAO:
            linhas.append(
                f"   - Meses {self._parcelas_taxa + 1} a 12 (Somente Aluguel Mensal):    "
                f"{formatar_moeda(aluguel_mensal):>13}/mês"
            )

        linhas.extend(
            [
                f"   - Total Acumulado em 12 Meses (Aluguel+Taxa):{formatar_moeda(total_primeiro_ano):>13}",
                "=" * 64,
            ]
        )
        return "\n".join(linhas)

    def exportar_csv(self, caminho_arquivo: str = "orcamento_rentsmart_12_meses.csv") -> str:
        """Exporta a projeção financeira dos 12 meses para um arquivo CSV."""
        projecao = self.gerar_projecao_12_meses()
        colunas = [
            "Mes",
            "Categoria_Imovel",
            "Aluguel_Mensal",
            "Parcela_Taxa_Contratual",
            "Status_Taxa_Contratual",
            "Total_Previsto_Mes",
        ]

        with open(caminho_arquivo, mode="w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=colunas, delimiter=";")
            escritor.writeheader()
            for linha in projecao:
                escritor.writerow(
                    {
                        "Mes": linha["Mes"],
                        "Categoria_Imovel": linha["Categoria_Imovel"],
                        "Aluguel_Mensal": f"{linha['Aluguel_Mensal']:.2f}",
                        "Parcela_Taxa_Contratual": f"{linha['Parcela_Taxa_Contratual']:.2f}",
                        "Status_Taxa_Contratual": linha["Status_Taxa_Contratual"],
                        "Total_Previsto_Mes": f"{linha['Total_Previsto_Mes']:.2f}",
                    }
                )
        return caminho_arquivo


# ==============================================================================
# 3. INTERFACE DE ATENDIMENTO E VALIDAÇÃO DE ENTRADAS (CLI)
# ==============================================================================


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


# ==============================================================================
# 4. BATERIA DE TESTES AUTOMATIZADOS (OPCIONAL: python rentsmart.py --testar)
# ==============================================================================


def executar_bateria_testes() -> None:
    """Valida todos os cenários comerciais previstos no enunciado."""
    cenarios = [
        (
            "Cenário 1: Apartamento de 1 quarto (sem garagem, com crianças, taxa em 1x)",
            Apartamento(quartos=1, possui_garagem=False, possui_criancas=True),
            1,
            700.00,
            2000.00,
        ),
        (
            "Cenário 2: Apartamento de 2 quartos com desconto (sem garagem, sem crianças, taxa em 5x)",
            Apartamento(quartos=2, possui_garagem=False, possui_criancas=False),
            5,
            855.00,
            400.00,
        ),
        (
            "Cenário 3: Casa de 2 quartos com garagem (taxa em 4x)",
            Casa(quartos=2, possui_garagem=True),
            4,
            1450.00,
            500.00,
        ),
        (
            "Cenário 4: Estúdio com pacote inicial de 2 vagas (taxa em 2x)",
            Estudio(incluir_pacote_vagas=True, vagas_adicionais=0),
            2,
            1450.00,
            1000.00,
        ),
        (
            "Cenário 5: Estúdio com pacote inicial + 3 vagas adicionais (taxa em 5x)",
            Estudio(incluir_pacote_vagas=True, vagas_adicionais=3),
            5,
            1630.00,
            400.00,
        ),
        (
            "Cenário 6: Apartamento 2 quartos com garagem e desconto (taxa em 3x)",
            Apartamento(quartos=2, possui_garagem=True, possui_criancas=False),
            3,
            1140.00,
            666.67,
        ),
    ]

    for titulo, imovel, parcelas, aluguel_esperado, parcela_esperada in cenarios:
        orc = OrcamentoLocacao(imovel=imovel, parcelas_taxa=parcelas)
        aluguel_calc = orc.imovel.calcular_aluguel_mensal()
        parcela_calc = orc.calcular_valor_parcela_taxa()

        assert aluguel_calc == aluguel_esperado, (
            f"Falha em {titulo}: esperado aluguel {aluguel_esperado}, obtido {aluguel_calc}"
        )
        assert parcela_calc == parcela_esperada, (
            f"Falha em {titulo}: esperada parcela {parcela_esperada}, obtida {parcela_calc}"
        )
        print(f"[OK] {titulo} -> Aluguel: R$ {aluguel_calc:.2f} | Parcela Taxa: R$ {parcela_calc:.2f}")

    print("\nTODOS OS 6 CENÁRIOS DE TESTE FORAM VALIDADOS COM SUCESSO!")


if __name__ == "__main__":
    if "--testar" in sys.argv:
        executar_bateria_testes()
    else:
        sistema = SistemaRentSmart()
        sistema.executar()