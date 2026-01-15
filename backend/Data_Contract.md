# ETF-Portfolio-Transparency-Overlap-Analyzer

Este projeto analisa a sobreposição de portfólios de ETFs a partir de um arquivo CSV de entrada.
O foco desta documentação é explicar exatamente como estruturar o CSV para que o sistema aceite e processe corretamente o portfólio.

1. Objetivo

Permitir que a usuária saiba como montar um arquivo CSV válido para uso no sistema, incluindo:

- Estrutura obrigatória de colunas;
- Regras de validação de dados;
- Mensagens de erro claras para facilitar correções;
- Exemplos de CSV válidos e inválidos.

2. Contrato de Dados (Data Contract) para o CSV

O arquivo deve estar em formato CSV (.csv) e obedecer ao contrato mínimo descrito a seguir:

## 2.1. Colunas Obrigatórias

O CSV deve conter as seguintes colunas no cabeçalho (linha 1):

| Coluna | Obrigatória | Tipo  | Descrição |
|--------|-------------|-------|-----------|
| symbol | Sim         | Texto | Símbolo/ticker do ETF (ex: VTI, SPY). |
| name   | Não         | Texto | Nome completo do ETF (ex: Vanguard Total Stock Market ETF). |
| weight | Sim         | Número| Peso percentual do ativo no portfólio (ex: 10, 10.5). |

Observações:

- O cabeçalho deve estar presente e, idealmente, na mesma ordem; colunas extras não são permitidas.
- A coluna `name` é opcional e não afeta os cálculos.

3. Regras de Validação

### 3.1. Formato do Arquivo

- O arquivo deve ser UTF-8;
- Deve ser separado por vírgulas (separator: ,);
- O cabeçalho deve conter pelo menos as colunas `symbol` e `weight`.

### 3.2. Validação de Colunas

O sistema fará as seguintes verificações:

- Todas as colunas obrigatórias estão presentes.
- Não existem colunas adicionais inesperadas.
- Os valores na coluna `weight` são numéricos positivos.

Se qualquer regra falhar, o arquivo é rejeitado com uma mensagem de erro clara.

### 3.3. Regras para a Coluna weight

Regra principal:

- Valores numéricos positivos;
- Aceita números inteiros (ex: 10) e decimais com ponto (ex: 10.5);
- Não aceita vírgula decimal, texto ou sinais negativos.

Exemplos válidos:
- 10
- 10.5
- 0

Exemplos inválidos:
- 10,5      ← vírgula em vez de ponto
- -5        ← valor negativo
- abc       ← texto

### 3.4. Soma dos Pesos

O padrão de mercado para tolerância em portfólios é permitir uma faixa em torno de 100% para acomodar pequenas imprecisões de arredondamento.
Portanto, adotamos:

99% ≤ soma(weights) ≤ 101%

Comportamento do Sistema:

- Se a soma total está dentro da faixa 99–101% → Válido;
- Se fora dessa faixa → Rejeitado com erro.

Mensagem de erro sugerida:

Soma total de weights inválida: <soma> — a soma deve estar entre 99 e 101 (tolerância de mercado)

4. Exemplos de CSV

### 4.1. CSV Válido
symbol,name,weight
VTI,Vanguard Total Stock Market ETF,30.0
VOO,Vanguard S&P 500 ETF,35
QQQ,Invesco QQQ Trust,35

Resultado:

Soma total de pesos: 100 → Dentro da faixa de tolerância → OK

### 4.2. CSV Válido com Decimais
symbol,name,weight
VTI,Vanguard Total Stock Market ETF,30.1
VOO,Vanguard S&P 500 ETF,35
QQQ,Invesco QQQ Trust,34.9

Resultado:

Soma total de pesos: 100.0 → Dentro da faixa de tolerância → OK

### 4.3. CSV Inválido — Peso Não Numérico
symbol,name,weight
VTI,Vanguard Total Stock Market ETF,30.0
VOO,Vanguard S&P 500 ETF,35
QQQ,Invesco QQQ Trust,abc

Erro esperado:

weight inválido na linha 4: valor 'abc' não é um número válido

### 4.4. CSV Inválido — Soma Fora da Tolerância
symbol,name,weight
VTI,Vanguard Total Stock Market ETF,40
VOO,Vanguard S&P 500 ETF,40
QQQ,Invesco QQQ Trust,40

Erro esperado:

Soma total de weights inválida: 120 — a soma deve estar entre 99 e 101 (tolerância de mercado)

5. Mensagens de Erro Claras

Para facilitar o uso e correção de arquivos CSV, o sistema deve apresentar mensagens de erro como:

- Coluna obrigatória ausente: <nome>
- Coluna não reconhecida: <nome>
- weight inválido na linha <n>: valor '<valor>' não é um número válido
- Soma total de weights inválida: <soma> — a soma deve estar entre 99 e 101 (tolerância de mercado)

6. Checklist de Aceite

Para que um CSV seja considerado aceito pelo sistema:

- Possui cabeçalho com colunas obrigatórias (`symbol`, `weight`);
- Não contém colunas extras;
- Todos os `weight` são numéricos e positivos;
- Soma dos `weight` está entre 99% e 101%.

7. Exemplo de Validação Automática (Opcional)

Se o projeto implementar uma rotina de validação, ela deve:

- Verificar cabeçalho;
- Validar cada linha de dados;
- Calcular a soma dos pesos;
- Retornar lista de erros (se houver);
- Indicar sucesso quando todas as regras forem satisfeitas.

8. Contato & Contribuição

Sugestões de melhoria ao contrato, exemplos adicionais ou dúvidas podem ser enviadas via issues no repositório.