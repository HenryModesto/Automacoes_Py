import pyautogui
import time

def main():
    print("=== DEPURADOR DE COORDENADAS ===")
    print("1. Este script ajudará a descobrir as coordenadas do seu ícone")
    print("2. Posicione o mouse sobre o ícone do Chrome quando solicitado")
    print("3. Não mova o mouse durante a captura")
    
    input("Pressione Enter quando estiver pronto...")
    
    print("\nPreparando para capturar em 3 segundos...")
    time.sleep(3)
    
    print("\nCAPTURANDO COORDENADAS EM 5...")
    time.sleep(1)
    print("4...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    
    posicao = pyautogui.position()
    print(f"\nCoordenadas capturadas: X={posicao.x} Y={posicao.y}")
    
    print("\nTestando clique nas coordenadas...")
    pyautogui.click(posicao.x, posicao.y)
    
    print("\nAtualize seu arquivo CSV com estas coordenadas:")
    print(f'Clicar no ícone,click,"{posicao.x},{posicao.y}"')

if __name__ == "__main__":
    main()