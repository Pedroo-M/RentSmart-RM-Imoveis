"""
Módulo de Orçamento e Projeção Financeira do Sistema RentSmart — R.M Imóveis.

Contém a classe OrcamentoLocacao, responsável por associar um objeto Imovel às
condições contratuais escolhidas, gerar o demonstrativo detalhado e exportar
a projeção financeira dos 12 primeiros meses de contrato em formato CSV.
"""

import csv
from models import Imovel


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
