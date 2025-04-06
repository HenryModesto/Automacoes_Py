import os
import time
from controller.automacao_controller import AutomacaoController

def configurar_ambiente():
    """Configura os caminhos dos arquivos"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return {
        'ARQUIVO_TAREFAS': os.path.join(base_dir, 'tarefas.csv'),
        'ARQUIVO_RELATORIO': os.path.join(base_dir, 'relatorio_execucao.xlsx')
    }

def verificar_arquivo_tarefas(caminho):
    """Verifica se o arquivo de tarefas existe"""
    if not os.path.exists(caminho):
        print(f"\n❌ Erro: Arquivo de tarefas não encontrado em:\n{caminho}")
        print("\nExemplo do formato necessário:")
        print("Tarefa,Tipo,Dado")
        print("Abrir Google Chrome,abrir_navegador,chrome")
        print("Clicar na barra de pesquisa,clicar,100,200")
        print("Digitar texto,digitar,Hello World")
        print("Pressionar Enter,tecla,enter")
        print("Esperar 5 segundos,esperar,5")
        return False
    return True

def main():
    """Função principal"""
    try:
        print("=== SISTEMA DE AUTOMAÇÃO ===")
        
        # Configura ambiente
        config = configurar_ambiente()
        
        # Verifica arquivo de tarefas
        if not verificar_arquivo_tarefas(config['ARQUIVO_TAREFAS']):
            input("Pressione Enter para sair...")
            return
        
        # Executa automação
        controller = AutomacaoController()
        inicio = time.time()
        
        print("\n▶ Iniciando execução das tarefas...")
        sucesso = controller.executar_fluxo(config)
        
        tempo_total = time.time() - inicio
        print(f"\n⏱ Tempo total: {tempo_total:.2f} segundos")
        
        if sucesso:
            print(f"\n✅ Relatório gerado com sucesso em:\n{config['ARQUIVO_RELATORIO']}")
        else:
            print("\n⚠ Ocorreram erros durante a execução - verifique o relatório")
        
        input("\nPressione Enter para sair...")
        
    except KeyboardInterrupt:
        print("\n⏹ Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()