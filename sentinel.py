import sqlite3
import socket
from datetime import datetime

def testar_porta(ip, porta):
    """Tenta conectar numa porta específica com timeout de 1 segundo"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.0)
    resultado = sock.connect_ex((ip, porta))
    sock.close()
    return "ABERTA" if resultado == 0 else "FECHADA"

# 1. Pega o IP local da interface
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_local = s.getsockname()[0]
    s.close()
except Exception:
    ip_local = "127.0.0.1"

hostname = socket.gethostname()
data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 2. Lista de portas para varredura de segurança
portas_alvo = [21, 22, 80, 443, 8080]

# 3. Conecta ao SQLite local
conn = sqlite3.connect('sentinel.db')
cursor = conn.cursor()

# Cria a tabela da Fase 2 para registrar o status das portas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS varredura_portas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_hora TEXT,
        ip_alvo TEXT,
        porta INTEGER,
        status TEXT
    )
''')

print("=" * 45)
print(f" SENTINEL FASE 2 - VARREDURA DE REDE [{data_hora}]")
print(f" Alvo: {ip_local} ({hostname})")
print("=" * 45)

# 4. Executa a varredura e grava no banco
for porta in portas_alvo:
    status = testar_porta(ip_local, porta)
    
    cursor.execute('''
        INSERT INTO varredura_portas (data_hora, ip_alvo, porta, status)
        VALUES (?, ?, ?, ?)
    ''', (data_hora, ip_local, porta, status))
    
    print(f"Porta {porta:<5} | Status: {status}")

conn.commit()
conn.close()

print("-" * 45)
print(" Varredura concluída e salva no SQLite com sucesso!")

		
