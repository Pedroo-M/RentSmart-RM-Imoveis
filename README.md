RentSmart — Sistema de Orçamento de Locação (R.M Imóveis)Aplicação em Python desenvolvida com Pensamento Algorítmico e Programação Orientada a Objetos (POO) para automatizar o cálculo de orçamentos de locação residencial da R.M Imóveis.1. Objetivo da AplicaçãoSubstituir o cálculo manual de orçamentos realizado pelos atendentes da R.M Imóveis por um sistema confiável, interativo e auditável. O RentSmart coleta as características do imóvel desejado pelo cliente, valida todas as entradas, aplica automaticamente as regras comerciais de adicionais, descontos e taxa contratual, exibe o demonstrativo detalhado no terminal e exporta uma projeção financeira de 12 meses em arquivo .csv.2. Tecnologias UtilizadasLinguagem: Python 3.10+Bibliotecas: Apenas biblioteca padrão do Python (csv e datetime), sem dependências externas.Paradigma: Programação Orientada a Objetos (Encapsulamento, Herança, Polimorfismo e Composição).3. Regras de Negócio ImplementadasCategoria / RegraCondição ComercialValor AplicadoApartamento (1 quarto)Aluguel-base mensalR$ 700,00Casa (1 quarto)Aluguel-base mensalR$ 900,00EstúdioAluguel-base mensalR$ 1.200,00Adicional 2 quartos (Apto)Acréscimo mensal para apartamentos de 2 quartos+ R$ 200,00Adicional 2 quartos (Casa)Acréscimo mensal para casas de 2 quartos+ R$ 250,00Garagem (Apto ou Casa)Inclusão opcional de vaga de garagem+ R$ 300,00Estacionamento (Estúdio)Pacote inicial de 2 vagas+ R$ 250,00Vaga adicional (Estúdio)Cada vaga extra além do pacote inicial de 2 vagas+ R$ 60,00 / vagaDesconto sem criançasExclusivo para Apartamentos, aplicado após adicionais− 5% sobre o subtotalTaxa ContratualEncargo fixo separado do aluguel, parcelável em 1x a 5xR$ 2.000,004. Arquitetura Orientada a Objetos e Estrutura dos Arquivosrentsmart-rm-imoveis/
├── rentsmart.py                         # Código-fonte principal com toda a modelagem POO
├── projecao_locacao_12_meses.csv        # Exemplo de planilha gerada automaticamente pelo sistema
├── documentacao_teorica_rentsmart.pdf   # Documentação acadêmica completa (IPO, Fluxograma, POO)
├── roteiro_video_pitch.md               # Roteiro estruturado para apresentação de até 4 minutos
└── README.md                            # Documentação técnica do repositório
Classes Implementadas em rentsmart.pyImovel: Classe base com atributos encapsulados (_categoria, _valor_base) e métodos polimórficos (calcular_adicionais, calcular_desconto, calcular_aluguel_mensal, detalhar_composicao).Apartamento(Imovel): Implementa adicionais de 2 quartos e garagem, além do desconto de 5% para locatários sem crianças.Casa(Imovel): Implementa adicionais de 2 quartos (+R$ 250,00) e garagem (+R$ 300,00).Estudio(Imovel): Implementa o pacote inicial de 2 vagas (+R$ 250,00) e o cálculo de vagas adicionais (+R$ 60,00 cada).OrcamentoLocacao: Agrega uma instância de Imovel, gerencia o parcelamento da taxa contratual de R$ 2.000,00 (1x a 5x), imprime o resumo discriminado e exporta o arquivo CSV de 12 meses.SistemaRentSmart: Controlador de interação CLI responsável pela validação defensiva das entradas do usuário.5. Instruções para Instalação e ExecuçãoCertifique-se de ter o Python 3 instalado em sua máquina (python --version ou python3 --version).Clone ou baixe este repositório para uma pasta local:git clone https://github.com/seu-usuario/rentsmart-rm-imoveis.git
cd rentsmart-rm-imoveis
Execute a aplicação diretamente pelo terminal:python rentsmart.py
(Em sistemas Linux/macOS, utilize python3 rentsmart.py se necessário.)6. Exemplo de UtilizaçãoSimulação de um Apartamento de 2 quartos, sem garagem, cliente sem crianças e taxa contratual parcelada em 4x:================================================================
       BEM-VINDO AO RENTSMART — R.M IMÓVEIS
   Sistema Automatizado de Orçamento de Locação (POO)
================================================================

Selecione a categoria do imóvel desejado:
  [1] Apartamento (Base: R$ 700,00)
  [2] Casa        (Base: R$ 900,00)
  [3] Estúdio     (Base: R$ 1.200,00)
Opção (1, 2 ou 3): 1
Quantidade de quartos (1 ou 2): 2
Deseja incluir vaga de garagem (+R$ 300,00)? [S/N]: N
O locatário possui crianças? (Sem crianças garante 5% de desconto) [S/N]: N

Taxa contratual obrigatória: R$ 2.000,00 (parcelável em até 5x).
Em quantas parcelas deseja pagar a taxa (1 a 5)? 4

================================================================
           R.M IMÓVEIS — RESUMO DO ORÇAMENTO RENTSMART
================================================================
Data da simulação : 22/11/2026 10:30
Categoria escolhida: Apartamento
----------------------------------------------------------------
1. COMPOSIÇÃO DO ALUGUEL MENSAL
   Aluguel-base (Apartamento): R$ 700,00
   + Adicional 2 quartos: R$ 200,00
   Subtotal mensal: R$ 900,00
   - Desconto de 5% (cliente sem crianças): -R$ 45,00
   >>> ALUGUEL MENSAL FINAL: R$ 855,00
----------------------------------------------------------------
2. TAXA CONTRATUAL (ENCARGO SEPARADO DO ALUGUEL)
   Valor total da taxa contratual: R$ 2.000,00
   Condição escolhida: 4x de R$ 500,00 (nos 4 primeiros meses)
----------------------------------------------------------------
3. SÍNTESE DO PRIMEIRO ANO (12 MESES)
   Meses 1 a 4 (Aluguel + Parcela da Taxa): R$ 1.355,00/mês
   Meses 5 a 12 (Somente Aluguel Mensal): R$ 855,00/mês
   Investimento total previsto em 12 meses: R$ 12.260,00
================================================================

[Sucesso] Projeção de 12 meses exportada para: 'projecao_locacao_12_meses.csv'.
7. Explicação do Arquivo CSV GeradoAo final de cada orçamento, o sistema gera o arquivo projecao_locacao_12_meses.csv (codificado em UTF-8-SIG e delimitado por ; para abertura imediata no Microsoft Excel, LibreOffice Calc ou Google Sheets). O arquivo contém 12 linhas correspondentes ao primeiro ano de contrato com as seguintes colunas:Mes: Identificação sequencial (Mês 1 a Mês 12).Categoria_Imovel: Categoria locada (Apartamento, Casa ou Estúdio).Aluguel_Mensal_BRL: Valor recorrente mensal líquido do imóvel.Parcela_Taxa_Contratual_BRL: Valor da parcela da taxa contratual ativa nos meses 1 a N e 0.00 após a quitação.Situacao_Taxa: Indica Parcela X/N durante o parcelamento ou Quitada nos meses restantes.Total_Previsto_Mes_BRL: Soma do aluguel mensal com a parcela da taxa naquele mês.Total_Acumulado_BRL: Desembolso acumulado do locatário até o respectivo mês.