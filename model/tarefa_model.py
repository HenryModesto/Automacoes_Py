import pandas as pd
import pyautogui
import time
import subprocess
import os
import platform
from datetime import datetime
from typing import Optional, Union, List, Dict

class TarefaModel:
    def __init__(self):
      
        pyautogui.PAUSE = 0.5
        pyautogui.FAILSAFE = True
        
        self.tentativas_maximas = 3
        self.confianca_imagem = 0.8
        self.timeout_padrao = 10
        
        self.caminhos_navegadores = {
            'chrome': [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                "chrome",
                "start chrome"
            ],
            'edge': [
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                "start msedge",
                "msedge"
            ]
        }

    def ler_tarefas(self, arquivo: str) -> pd.DataFrame:
        """
        Lê arquivo de tarefas com tratamento robusto
        
        Args:
            arquivo: Caminho do arquivo (CSV ou Excel)
            
        Returns:
            DataFrame com as tarefas
            
        Raises:
            FileNotFoundError: Se arquivo não existe
            ValueError: Se formato for inválido
        """
        if not os.path.exists(arquivo):
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")
        
        try:
            if arquivo.endswith('.csv'):
                return pd.read_csv(arquivo, quotechar='"', engine='python')
            elif arquivo.endswith(('.xlsx', '.xls')):
                return pd.read_excel(arquivo)
            else:
                raise ValueError("Formato deve ser CSV ou Excel")
        except Exception as e:
            raise ValueError(f"Erro ao ler arquivo: {str(e)}")

    def executar_acao(self, tipo: str, dado: str) -> Dict:
        """
        Executa uma ação com tratamento completo de erros
        
        Args:
            tipo: Tipo de ação (abrir_navegador, click, etc)
            dado: Parâmetro da ação
            
        Returns:
            Dict com {'status': str, 'mensagem': str, 'tempo': float}
        """
        inicio = time.time()
        resultado = {
            'status': 'Falha',
            'mensagem': '',
            'tempo': 0
        }
        
        try:
            if not tipo or not dado:
                raise ValueError("Tipo e dado são obrigatórios")
                
            tipo = tipo.lower().strip()
            dado = str(dado).strip()
            
            if tipo == 'abrir_navegador':
                self._abrir_navegador(dado)
            elif tipo == 'click':
                self._executar_click(dado)
            elif tipo == 'texto':
                self._digitar_texto(dado)
            elif tipo == 'tecla':
                self._pressionar_tecla(dado)
            elif tipo == 'hotkey':
                self._executar_hotkey(dado)
            elif tipo == 'espera':
                self._esperar(dado)
            elif tipo == 'comando':
                self._executar_comando(dado)
            else:
                raise ValueError(f"Tipo de ação não suportado: {tipo}")
            
            resultado['status'] = 'Sucesso'
            
        except Exception as e:
            resultado['mensagem'] = str(e)
        finally:
            resultado['tempo'] = round(time.time() - inicio, 2)
            
        return resultado

    def _abrir_navegador(self, navegador: str) -> None:
        """Abre navegador com fallback para diferentes caminhos"""
        navegador = navegador.lower()
        if navegador not in self.caminhos_navegadores:
            raise ValueError(f"Navegador não suportado: {navegador}")
            
        for caminho in self.caminhos_navegadores[navegador]:
            try:
                if os.path.exists(caminho) or ' ' not in caminho:
                    subprocess.Popen(caminho, shell=True)
                    time.sleep(5)
                    return
            except:
                continue
                
        raise Exception(f"Não foi possível abrir {navegador}")

    def _executar_click(self, dado: str) -> None:
        """Executa click em coordenadas ou imagem"""
        if ',' in dado:  # Coordenadas
            try:
                x, y = map(int, dado.split(','))
                self._mover_e_clicar(x, y)
            except ValueError:
                raise ValueError("Coordenadas devem ser no formato 'x,y'")
        else:  
            encontrado = False
            for _ in range(self.tentativas_maximas):
                try:
                    loc = pyautogui.locateCenterOnScreen(
                        f'{dado}.png',
                        confidence=self.confianca_imagem,
                        minSearchTime=1
                    )
                    if loc:
                        self._mover_e_clicar(loc.x, loc.y)
                        encontrado = True
                        break
                except:
                    time.sleep(1)
            
            if not encontrado:
                raise ValueError(f"Elemento '{dado}' não encontrado")

    
    def executar_fluxo(
        self,
        tarefas: Union[pd.DataFrame, List[Dict]],
        intervalo: float = 1.0
    ) -> pd.DataFrame:
        """
        Executa um fluxo completo de tarefas
        
        Args:
            tarefas: DataFrame ou lista de dicionários com tarefas
            intervalo: Tempo entre tarefas
            
        Returns:
            DataFrame com relatório de execução
        """
        from relatorio_model import RelatorioModel  # Importação local para evitar circular
        
        relatorio = RelatorioModel()
        df = relatorio.criar_relatorio()
        
        # Converte para lista de dicionários se for DataFrame
        if isinstance(tarefas, pd.DataFrame):
            tarefas = tarefas.to_dict('records')
            
        for tarefa in tarefas:
            try:
                resultado = self.executar_acao(
                    tarefa.get('Tipo'),
                    tarefa.get('Dado')
                )
                
                df = relatorio.adicionar_tarefa_relatorio(
                    df,
                    tarefa.get('Tarefa', ''),
                    tarefa.get('Tipo', ''),
                    tarefa.get('Dado', ''),
                    resultado['status'],
                    resultado['tempo'],
                    resultado.get('mensagem')
                )
                
                time.sleep(intervalo)
                
            except Exception as e:
                print(f"Erro ao executar tarefa {tarefa}: {str(e)}")
                continue
                
        return df