"""
Script de Validação dos Cenários de Teste do RentSmart — R.M Imóveis.

Testa automaticamente todos os cenários comerciais previstos no enunciado e gera
o arquivo CSV de exemplo oficial para o repositório.
"""

from models import Apartamento, Casa, Estudio
from orcamento import OrcamentoLocacao


def executar_bateria_testes() -> None:
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
            855.00,  # (700 + 200) * 0.95 = 855.00
            400.00,
        ),
        (
            "Cenário 3: Casa de 2 quartos com garagem (taxa em 4x)",
            Casa(quartos=2, possui_garagem=True),
            4,
            1450.00,  # 900 + 250 + 300 = 1450.00
            500.00,
        ),
        (
            "Cenário 4: Estúdio com pacote inicial de 2 vagas (taxa em 2x)",
            Estudio(incluir_pacote_vagas=True, vagas_adicionais=0),
            2,
            1450.00,  # 1200 + 250 = 1450.00
            1000.00,
        ),
        (
            "Cenário 5: Estúdio com pacote inicial + 3 vagas adicionais (taxa em 5x)",
            Estudio(incluir_pacote_vagas=True, vagas_adicionais=3),
            5,
            1630.00,  # 1200 + 250 + (3 * 60) = 1630.00
            400.00,
        ),
        (
            "Cenário 6: Apartamento 2 quartos com garagem e desconto (taxa em 3x)",
            Apartamento(quartos=2, possui_garagem=True, possui_criancas=False),
            3,
            1140.00,  # (700 + 200 + 300) * 0.95 = 1140.00
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

        print(f"\n>>> {titulo}")
        print(orc.gerar_resumo_formatado())

        if "Cenário 2" in titulo:
            orc.exportar_csv("exemplo_orcamento.csv")
            print("[OK] CSV de exemplo gerado: exemplo_orcamento.csv")


if __name__ == "__main__":
    executar_bateria_testes()
    print("\nTODOS OS 6 CENÁRIOS DE TESTE FORAM VALIDADOS COM SUCESSO!")
