# Desafio MBA Engenharia de Software com IA - Full Cycle

## Passo a passo para rodar o projeto

### 1. Criar e ativar o ambiente virtual
python3 -m venv venv
source venv/bin/activate

### 2. Configurar variáveis de ambiente
- Faça uma cópia do arquivo .env.example e renomeie para .env.
- Preencha as variáveis:

  - OPENAI_API_KEY ou GOOGLE_API_KEY
    > Se informar ambas, o OpenAI terá prioridade.
  - DATABASE_URL: URL de conexão com o banco Postgres (rodando no Docker).
  - PDF_PATH: Caminho absoluto para o arquivo PDF a ser ingerido.
    - Para teste, pode usar o arquivo document.pdf já incluso no repositório.

### 3. Subir o banco de dados com Docker
docker compose up -d

### 4. Fazer a ingestão do PDF
python3 src/ingest.py
O script nã faz nova ingestão se já houver dados no banco.
> Observação: Ele não contempla múltiplos documentos: Se já existir informação, não insere novamente.

### 5. Rodar o chat
python3 src/chat.py

## Observações
- O projeto já vem com um document.pdf de exemplo.
- Certifique-se de que as chaves de API estão corretas antes de rodar.
- O banco de dados usa a extensão pgvector, já configurada no docker-compose.yml.