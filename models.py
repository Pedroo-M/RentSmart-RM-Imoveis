"""
Módulo de Modelos de Domínio do Sistema RentSmart — R.M Imóveis.

Define a hierarquia de classes de imóveis utilizando Programação Orientada a Objetos
(abstração, encapsulamento, herança e polimorfismo) para representar as regras
comerciais de locação de Apartamentos, Casas e Estúdios.
"""

from abc import ABC, abstractmethod


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
