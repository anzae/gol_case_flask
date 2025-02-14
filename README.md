# Case Desenvolvedor GOL - Instruções

A partir dos dados públicos da ANAC (Dados_Estatisticos.csv), fazer uma aplicação web considerando os passos:

Base de dados: https://sistemas.anac.gov.br/dadosabertos/Voos%20e%20opera%C3%A7%C3%B5es%20a%C3%A9reas/Dados%20Estat%C3%ADsticos%20do%20Transporte%20A%C3%A9reo/

### Crie um banco de dados SQL com a tabela com informações a seguir

1. Filtros:
- cia aérea GOL: EMPRESA = "GLO";
- voos regulares: GRUPO_DE_VOO = "REGULAR";
- voos do Brasil: NATUREZA = "DOMÉSTICA".

2. Agrupar informações de voos ida e volta, criando a coluna MERCADO:
- MERCADO = AEROPORTO DE ORIGEM + AEROPORTO DE DESTINO, em ordem alfabética.

3. Colunas da tabela:
- ANO
- MES
- MERCADO
- RPK

### Aplicação Web

- Autenticação do usuário (login)
- Filtro para selecionar o mercado
- Filtro para selecionar o intervalo de datas
- Gráfico do RPK (eixo y) por data (eixo x), para o mercado e intervalo de datas


---
# Case Desenvolvedor GOL - Solução

## Criação da tabela
- Para criar o banco de dados, coloque o arquivo ```Dados_Estatisticos.csv``` dentro da pasta ```data/```, na raiz do projeto.
- Executar o arquivo ```import_data.py```.
- Isso criará um banco de dados ```voos.db``` dentro da pasta ```instance/```.

## Aplicação Web 
- Executar o arquivo ```app.py```.
- A aplicação será executada localmente em ```localhost:5000```.
- Criar usuário em ```localhost:5000/login``` -> clicar em "Registrar".
- Fazer login em ```localhost:5000/login```.
- Acessar ```localhost:5000```, o app estará funcionando após autenticação.