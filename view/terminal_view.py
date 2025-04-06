class TerminalView:
    @staticmethod
    def mostrar_mensagem(mensagem):
        print(f">>> {mensagem}")

    @staticmethod
    def mostrar_erro(mensagem):
        print(f"\033[91m[ERRO] {mensagem}\033[0m")

    @staticmethod
    def mostrar_alerta(mensagem):
        print(f"\033[93m[ALERTA] {mensagem}\033[0m")

    @staticmethod
    def mostrar_sucesso(mensagem):
        print(f"\033[92m[SUCESSO] {mensagem}\033[0m")

    @staticmethod
    def solicitar_confirmacao(mensagem):
        resposta = input(f"{mensagem} (s/n): ").lower()
        return resposta == 's'

    @staticmethod
    def mostrar_resumo_execucao(total, sucessos, falhas, tempo_total):
        print("\n=== RESUMO DA EXECUÇÃO ===")
        print(f"Tarefas totais: {total}")
        print(f"\033[92mSucessos: {sucessos}\033[0m")
        print(f"\033[91mFalhas: {falhas}\033[0m")
        print(f"Tempo total: {tempo_total:.2f} segundos")