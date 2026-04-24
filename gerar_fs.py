import os
from littlefs import LittleFS

# Configura um sistema de arquivos de 2MB (padrão para a partição que você definiu)
fs = LittleFS(block_size=4096, block_count=512)

# Se você estiver usando a pasta src/
pasta_codigo = 'src' 

# Lê o seu main.py como binário ('rb')
with open(f'{pasta_codigo}/main.py', 'rb') as f:
    conteudo = f.read()
    
# GERA O ARQUIVO NO HD VIRTUAL COMO BINÁRIO TAMBÉM ('wb' em vez de 'w')
with fs.open('main.py', 'wb') as f:
    f.write(conteudo)

# Salva o resultado final no arquivo físico fs.bin
with open('fs.bin', 'wb') as f:
    f.write(fs.context.buffer)

print("✅ Arquivo fs.bin gerado com sucesso!")