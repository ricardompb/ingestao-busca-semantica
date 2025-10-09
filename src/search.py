from envloader import load_env, get_llm
from langchain_postgres import PGVector
from langchain.schema import HumanMessage

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt():
  env = load_env()
  llm = get_llm(env)

  store = PGVector(embeddings=env["EMBEDDINGS"],
          collection_name=env["PG_VECTOR_COLLECTION_NAME"],
          connection=env["DATABASE_URL"], 
          use_jsonb=True)

  def run(pergunta):
    # Busca os 10 mais relevantes
    results = store.similarity_search_with_score(pergunta, k=10)
    # Extrai o texto dos resultados
    contexto = "\n\n".join([doc.page_content for doc, score in results])
    prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=pergunta)
    # llm faz a resposta
    resposta =  llm.invoke([HumanMessage(content=prompt)])
    return resposta.content

  class Chain:
    def run(self, pergunta):
      return run(pergunta)
  return Chain()