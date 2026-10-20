import sqlite3
from flask import Flask

app = Flask(__name__)

def buscar_dados():
    """Conecta no banco SQLite e busca todas as varreduras"""
    conn = sqlite3.connect('sentinel.db')
    cursor = conn.cursor()
    cursor.execute("SELECT data_hora, ip_alvo, porta, status FROM varredura_portas ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados

@app.route('/')
def dashboard():
    registros = buscar_dados()
    
    # Monta a página HTML simples diretamente em Python
    html = '''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Termux Sentinel - Dashboard</title>
        <style>
            body { font-family: monospace; background-color: #121212; color: #00ff66; padding: 20px; }
            h1 { border-bottom: 2px solid #00ff66; padding-bottom: 10px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #00ff66; padding: 10px; text-align: left; }
            th { background-color: #1e1e1e; }
            tr:nth-child(even) { background-color: #1a1a1a; }
            .fechada { color: #ff5555; }
            .aberta { color: #00ff66; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>🛡️ Termux Sentinel - Painel de Segurança</h1>
        <p>Servidor rodando nativamente no Android via Flask + SQLite</p>
        
        <table>
            <tr>
                <th>Data / Hora</th>
                <th>IP Alvo</th>
                <th>Porta</th>
                <th>Status</th>
            </tr>
    '''
    
    for r in registros:
        classe_status = "aberta" if r[3] == "ABERTA" else "fechada"
        html += f'''
            <tr>
                <td>{r[0]}</td>
                <td>{r[1]}</td>
                <td>{r[2]}</td>
                <td class="{classe_status}">{r[3]}</td>
            </tr>
        '''
        
    html += '''
        </table>
    </body>
    </html>
    '''
    return html

if __name__ == '__main__':
    print("Servidor Flask rodando! Acesse no navegador: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000)
