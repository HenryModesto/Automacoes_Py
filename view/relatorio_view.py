from typing import Optional

class RelatorioView:
    @staticmethod
    def mostrar_mensagem(mensagem: str, tipo: str = 'info') -> None:
        """
        Exibe mensagens coloridas no console
        
        Args:
            mensagem: Texto a ser exibido
            tipo: 'info', 'sucesso', 'erro', 'alerta'
        """
        cores = {
            'info': '\033[94m',     # Azul
            'sucesso': '\033[92m',  # Verde
            'erro': '\033[91m',     # Vermelho
            'alerta': '\033[93m'    # Amarelo
        }
        reset = '\033[0m'
        
        print(f"{cores.get(tipo, cores['info'])}{mensagem}{reset}")

    @staticmethod
    def mostrar_erro_detalhado(
        mensagem: str,
        erro: Optional[Exception] = None,
        detalhes: Optional[str] = None
    ) -> None:
        """Exibe erros com detalhes técnicos"""
        print(f"\033[91mERRO: {mensagem}\033[0m")
        if erro:
            print(f"\033[93mTipo: {type(erro).__name__}\033[0m")
        if detalhes:
            print(f"\033[93mDetalhes: {detalhes}\033[0m")

    @staticmethod
    def mostrar_relatorio(df, limite: int = 10) -> None:
        """Exibe preview do relatório"""
        if df.empty:
            print("\033[93mRelatório vazio\033[0m")
        else:
            print(f"\033[94mPreview do relatório ({min(len(df), limite)} linhas):\033[0m")
            print(df.head(limite).to_string(index=False))