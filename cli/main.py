import pynput # biblioteca para controlar e monitor device io como mouse e teclado
import pyautogui as pg # biblioteca de automação
import threading # joga a execução do código para um "terminal" do python para poder continuar usando o teclado/mouse
import random # biblioteca para pressionar com o tempo variável similando uma ação humana, ela é necessária pra gerar números aleatórios
pg.ImageNotFoundException(False) # exceção quando a função da pg não consiga encontrar a imagem na tela (o tibia fica com a tela preta, fazendo com que esse script não precise da tela do tibia)

FULL_DEFENSIVE_HOTKEY = {"hotkey":'-', "delay": random.uniform(0.1, 2.5)} # constante da hk fulldef
FULL_OFFENSIVE_HOTKEY = {"hotkey":'=', "delay": random.uniform(0.1, 0.8)} # constante da hk fullatk
USE_RING_HOTKEY = {"hotkey":'F1', "delay": random.uniform(0.2, 1.1)} # constante da hk do ring, no assign tem que marcar a caixinha SMART MODE
FOOD_HOTKEY = 'F12' # hk pra comer food

list_hotkey_before = [FULL_OFFENSIVE_HOTKEY, USE_RING_HOTKEY] # array com as const da fk fullatk e ring
list_hotkey_after = [FULL_DEFENSIVE_HOTKEY, USE_RING_HOTKEY]# array com as const da fk fulldef e ring

LIST_HOTKEYS_ATTACKS = {"hotkey":'F1', "delay": random.uniform(0.1, 0.3)}, # sempre chave valor, hotkey é chave e F1 é o valor
{"hotkey":'F1', "delay": random.uniform(0.2, 0.5)}, # random.uniform(x, y) gera um número aleaório entre x e y
{"hotkey":'F1', "delay": random.uniform(0.1, 0.6)},
{"hotkey":'F1', "delay": random.uniform(0.1, 0.3)},
{"hotkey":'F1', "delay": random.uniform(0.2, 0.3)},
{"hotkey":'F1', "delay": random.uniform(0.1, 0.4)},
{"hotkey":'F1', "delay": random.uniform(0.2, 0.5)},
{"hotkey":'F1', "delay": random.uniform(0.1, 0.3)},
{"hotkey":'F1', "delay": random.uniform(0.1, 0.6)},
{"hotkey":'F12', "delay": random.uniform(0.1, 0.6)} # hk das skills pra rotação, o delay é a demora até soltar a skill de novo

def rotate_skills():
    while not event_rotate_skills.is_set(): # seta a thread
        for attack in LIST_HOTKEYS_ATTACKS: # for que passa no array da lista e executa todos os encontrados
            if event_rotate_skills.is_set(): # se a thread for true
                return
            pg.press(attack["hotkey"]) # executa a hotkey encontrada no array
            pg.sleep(attack["delay"]) # executa o delay encontrada no array

def execute_hotkey(hotkey): # hk de modo attack e modo defensive, set to defensive: - /// set to offensive: =
    pg.press(hotkey)

running = False
def key_code(key):
    global running
    print('Key ->', key)
    if key == pynput.keyboard.Key.delete: # delete para parar o helper
        print('Bot encerrado')
        return False
    if hasattr(key, 'char') and key.char == 'r': # tecla r para começar a rotação de skills
        if running == False:
            running = True
            global th_rotate_skills, event_rotate_skills
            event_rotate_skills = threading.Event()
            th_rotate_skills = threading.Thread(target=rotate_skills) # linka a thread na rotate_skills
            print('Iniciando a rotação de skills') # primeiro f começa a rotação de skills
            for hotkey in list_hotkey_before: # coloca o ring e altera pro modo fullatk
                execute_hotkey(hotkey)
            th_rotate_skills.start() # inicia a thread
        else:
            running = False
            event_rotate_skills.set()
            th_rotate_skills.join() # espera a thread terminar
            print('Parando rotação de skills') # segundo f para a rotação de skills
            for hotkey in list_hotkey_after: # tira o ring e altera pro modo fulldef
                execute_hotkey(hotkey)

with pynput.keyboard.Listener(on_press=key_code) as listener:
    listener.join()
