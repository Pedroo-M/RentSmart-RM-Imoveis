# 🏠 RentSmart — Sistema de Orçamento de Locação (R.M Imóveis)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Paradigma](https://img.shields.io/badge/Paradigma-POO%20%2F%20OOP-0D7377?style=for-the-badge)
![Dependências](https://img.shields.io/badge/Dependências-Zero%20(Stdlib)-1E5631?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)

Aplicação desenvolvida em **Python** aplicando os fundamentos de **Pensamento Algorítmico (*Algorithmic Thinking*)** e **Programação Orientada a Objetos (*Object-Oriented Programming*)** para automatizar, padronizar e auditar o cálculo de orçamentos de locação residencial da **R.M Imóveis**.

---

## 📋 Índice

- [1. Problema e Objetivo da Aplicação](#-1-problema-e-objetivo-da-aplicação)
- [2. Tecnologias e Conceitos Aplicados](#-2-tecnologias-e-conceitos-aplicados)
- [3. Regras de Negócio Implementadas](#-3-regras-de-negócio-implementadas)
- [4. Arquitetura Orientada a Objetos e Estrutura do Projeto](#-4-arquitetura-orientada-a-objetos-e-estrutura-do-projeto)
- [5. Instalação e Execução](#-5-instalação-e-execução)
- [6. Exemplo de Utilização](#-6-exemplo-de-utilização)
- [7. Estrutura do Arquivo CSV Gerado](#-7-estrutura-do-arquivo-csv-gerado)

---

## 🎯 1. Problema e Objetivo da Aplicação

Com o crescimento da carteira de imóveis e do volume de atendimentos da **R.M Imóveis**, o cálculo manual de cotações de locação tornou-se lento e vulnerável a falhas humanas na aplicação de adicionais, descontos promocionais e condições de parcelamento contratual.

O **RentSmart** resolve esse gargalo operacional por meio de um fluxo interativo em linha de comando (CLI) que:
- **Coleta e valida** defensivamente todas as características do imóvel desejado pelo cliente;
- **Aplica automaticamente** valores-base, adicionais (quartos, garagem/vagas) e descontos comerciais;
- **Separa explicitamente** o **aluguel mensal recorrente** da **taxa contratual** (R$ 2.000,00 parceláveis em até 5x);
- **Exibe um demonstrativo auditável** da composição do orçamento no terminal;
- **Cria e lê um arquivo `.csv`** com a projeção financeira mês a mês dos **12 primeiros meses** de contrato.

---

## 🛠️ 2. Tecnologias e Conceitos Aplicados

| Recurso | Detalhamento |
| :--- | :--- |
| **Linguagem** | Python 3.10 ou superior |
| **Bibliotecas** | Apenas biblioteca padrão (`abc`, `csv`, `os`, `sys`) — **zero dependências externas** |
| **Pilares de POO** | **Abstração** (`ABC` / `@abstractmethod`), **Encapsulamento** (`@property` e atributos protegidos), **Herança**, **Polimorfismo** e **Composição** |
| **Pensamento Algorítmico** | Decomposição modular, validação defensiva em laços (`while True`), tratamento de exceções e persistência tabular |

---

## 📊 3. Regras de Negócio Implementadas

| Categoria / Regra | Condição Comercial | Valor / Regra Aplicada |
| :--- | :--- | :---: |
| **Apartamento (1 quarto)** | Aluguel-base mensal | **R$ 700,00** |
| **Casa (1 quarto)** | Aluguel-base mensal | **R$ 900,00** |
| **Estúdio** | Aluguel-base mensal | **R$ 1.200,00** |
| **Adicional 2 quartos (Apto)** | Acréscimo mensal para apartamentos de 2 quartos | **+ R$ 200,00** |
| **Adicional 2 quartos (Casa)** | Acréscimo mensal para casas de 2 quartos | **+ R$ 250,00** |
| **Garagem (Apto ou Casa)** | Inclusão opcional de 1 vaga de garagem | **+ R$ 300,00** |
| **Estacionamento (Estúdio)** | Pacote inicial obrigatório para estacionamento (2 vagas) | **+ R$ 250,00** |
| **Vaga adicional (Estúdio)** | Cada vaga extra além do pacote inicial de 2 vagas | **+ R$ 60,00 / vaga** |
| **Desconto sem crianças** | Exclusivo para **Apartamentos**, aplicado sobre o subtotal (após adicionais) | **− 5%** |
| **Taxa Contratual** | Encargo fixo cobrado separadamente do aluguel, parcelável de `1x` a `5x` | **R$ 2.000,00** |

---

## 🏗️ 4. Arquitetura Orientada a Objetos e Estrutura do Projeto

### Estrutura de Arquivos

```text
rentsmart-rm-imoveis/
├── rentsmart.py                       # Aplicação principal (POO, CLI, criação/leitura CSV e testes)
├── orcamento_apartamento_12_meses.csv # Exemplo de planilha gerada automaticamente pelo sistema
├── documentacao_teorica_rentsmart.pdf # Documentação acadêmica (Análise, IPO, Fluxograma e POO)
├── roteiro_video_pitch.md             # Roteiro estruturado para apresentação em vídeo (até 4 min)
└── README.md                          # Documentação técnica do repositório
