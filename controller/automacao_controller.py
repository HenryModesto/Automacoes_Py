import pandas as pd
import pyautogui
import time
import subprocess
import os
from datetime import datetime
from model.relatorio_model import RelatorioModel

class AutomacaoController:
    def __init__(self):
        self.relatorio = RelatorioModel()
        self.tentativas_maximas = 3
        pyautogui.PAUSE = 1

    def executar_fluxo(self, config):
        """Executa todo o fluxo de automação"""
        try:
            tarefas = self._ler_tarefas(config['ARQUIVO_TAREFAS'])
            
            df_relatorio = self.relatorio.criar_relatorio()
            
            for index, tarefa in tarefas.iterrows():
                inicio = time.time()
                
                try:
                    resultado = self._executar_acao(
                        tarefa['Tipo'],
                        tarefa['Dado']
                    )
                    status = "Sucesso"
                    mensagem = ""
                except Exception as e:
                    status = "Falha"
                    mensagem = str(e)
                
                tempo_execucao = round(time.time() - inicio, 2)
                
                df_relatorio = self.relatorio.adicionar_tarefa_relatorio(
                    df_relatorio,
                    tarefa['Tarefa'],
                    tarefa['Tipo'],
                    tarefa['Dado'],
                    status,
                    tempo_execucao
                )
            
            self.relatorio.salvar_relatorio(df_relatorio, config['ARQUIVO_RELATORIO'])
            return True
            
        except Exception as e:
            print(f"Erro durante a execução do fluxo: {str(e)}")
            return False

    def _ler_tarefas(self, caminho):
        """Lê o arquivo CSV de tarefas com validação"""
        try:
            df = pd.read_csv(caminho)
            if not all(col in df.columns for col in ['Tarefa', 'Tipo', 'Dado']):
                raise ValueError("Arquivo de tarefas deve conter colunas: Tarefa, Tipo, Dado")
            return df
        except Exception as e:
            raise ValueError(f"Erro ao ler arquivo de tarefas: {str(e)}")

    def _executar_acao(self, tipo, dado):
        """Executa uma ação específica com tratamento robusto"""
        tipo = tipo.lower().strip()
        dado = str(dado).strip()

        try:
            if tipo == 'espera':
                self._esperar(dado)
            elif tipo == 'comando':
                self._executar_comando(dado)
            elif tipo == 'texto':
                self._digitar_texto(dado)
            elif tipo == 'tecla':
                self._pressionar_tecla(dado)
            elif tipo == 'click':
                self._clicar(dado)
            else:
                raise ValueError(f"Tipo de ação não suportado: {tipo}")
        except Exception as e:
            raise Exception(f"Falha ao executar '{tipo} {dado}': {str(e)}")

    def _clicar(self, coordenadas):
        """Clica nas coordenadas x,y com tratamento de erro"""
        try:
            x, y = map(int, coordenadas.split(','))
            pyautogui.click(x, y)
            time.sleep(1)  
        except Exception as e:
            raise ValueError(f"Coordenadas inválidas: {coordenadas}. Erro: {str(e)}")

    def _digitar_texto(self, texto):
        """Digita texto com tratamento especial"""
        try:
            pyautogui.write(texto, interval=0.1)
            time.sleep(0.5)
        except Exception as e:
            raise Exception(f"Falha ao digitar texto: {str(e)}")

    def _pressionar_tecla(self, tecla):
        """Pressiona tecla com validação"""
        try:
            pyautogui.press(tecla.lower())
            time.sleep(0.5)
        except Exception as e:
            raise Exception(f"Falha ao pressionar tecla: {str(e)}")

    def _esperar(self, segundos):
        """Espera tempo especificado"""
        try:
            segundos = float(segundos)
            if segundos > 0:
                time.sleep(segundos)
        except ValueError:
            raise ValueError(f"Tempo de espera inválido: {segundos}")

    def _executar_comando(self, comando):
        """Executa comando no sistema"""
        try:
            subprocess.Popen(comando, shell=True)
            time.sleep(2) 
        except Exception as e:
            raise Exception(f"Falha ao executar comando: {str(e)}")

    def encontrar_coordenadas(self):
        """Método auxiliar para encontrar coordenadas da barra de pesquisa"""
        print("Posicione o mouse na barra de pesquisa e aguarde 5 segundos...")
        time.sleep(5)
        x, y = pyautogui.position()
        print(f"Coordenadas encontradas: {x},{y}")
        return x, y