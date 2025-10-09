from search import search_prompt

def main():
    # Iniciar o chat
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    print("=== Chat iniciado ===")
    print("Digite 'sair' para encerrar o chat.")

    while True:
        pergunta = input("\nVocê: ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o chat...")
            break

        try:
            resposta = chain.run(pergunta)  
            print(f"IA: {resposta}")
        except Exception as e:
            print(f"Ocorreu um erro ao processar sua pergunta: {e}")

if __name__ == "__main__":
    main()