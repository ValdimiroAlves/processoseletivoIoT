from machine import Pin, ADC
import time
import math
import sys 

# ==========================================
# 1. CONFIGURAÇÃO DE HARDWARE
# ==========================================
led = Pin(2, Pin.OUT)
botao = Pin(4, Pin.IN, Pin.PULL_UP)

# Sensor LDR no pino 34 
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB) 

# Constantes do Sensor 
GAMMA = 0.7
RL10 = 50
 
# ==========================================
# 2. VARIÁVEIS DE CONTROLE E TEMPO
# ========================================== 
modo_auto = True
ultimo_estado_botao = 1
tempo_ultimo_print = time.ticks_ms()

# Variáveis para o Encerramento Automático 
ciclos_execucao = 0
LIMITE_CICLOS = 200 

def ler_lux():
    #Calcula o Lux
    analogValue = ldr.read()
    
    if analogValue == 0:
        return 0.1
        
    voltage = analogValue / 4095.0 * 3.3
    
    if voltage >= 3.3: 
        voltage = 3.299
        
    resistance = 2000 * voltage / (1 - voltage / 3.3)
    
    try:
        numerador = RL10 * 1000 * math.pow(10, GAMMA)
        lux = math.pow(numerador / resistance, (1 / GAMMA))
        return int(round(lux, 0))
    except:
        return 0

print("Simulação Iniciada! ")

# ==========================================
# 3. LOOP PRINCIPAL
# ==========================================
while True:
    try:
        # LÓGICA DO BOTÃO
        estado_atual_botao = botao.value()
        
        if estado_atual_botao == 0 and ultimo_estado_botao == 1:
            modo_auto = not modo_auto 
            
            if not modo_auto:
                led.value(not led.value())
                print("\n[EVENTO] MODO MANUAL ATIVADO")
            else:
                print("\n[EVENTO] MODO AUTOMÁTICO ATIVADO")
                
            time.sleep(0.2)
            
        ultimo_estado_botao = estado_atual_botao

        # LÓGICA DO SENSOR (APENAS EM MODO AUTO)
        lux_atual = ler_lux()

        if modo_auto:
            if lux_atual < 100:
                led.value(1) # Liga se Lux < 100
            else:
                led.value(0) # Desliga se Lux >= 100

        # LOG NO TERMINAL A CADA 2 SEGUNDOS
        tempo_atual = time.ticks_ms()
        if time.ticks_diff(tempo_atual, tempo_ultimo_print) >= 2000:
            status_m = "AUTO" if modo_auto else "MANU"
            status_l = "LIGADO" if led.value() == 1 else "DESLIGADO"
            print(f"STATUS: Modo={status_m} | Luz={lux_atual:4} Lux | LED={status_l}")
            tempo_ultimo_print = tempo_atual

        # CONTROLE DE ENCERRAMENTO AUTOMÁTICO
        ciclos_execucao += 1
        if ciclos_execucao >= LIMITE_CICLOS:
            print("\n Tempo de teste atingido. Encerrando simulação com sucesso.")
            sys.exit() 

        time.sleep(0.05)

    except SystemExit:
        raise
    except Exception as e:
        print(f"Erro inesperado: {e}")
        time.sleep(1)