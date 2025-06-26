# servidor_webchat.py
import asyncio
import websockets
import json
import logging
from datetime import datetime

# Configura um logger básico
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Conjunto (set) para armazenar todas as conexões de clientes ativos
CONNECTED_CLIENTS = set()

async def broadcast(message):
    """ Envia uma mensagem para todos os clientes conectados. """
    if CONNECTED_CLIENTS:
        await asyncio.gather(*[client.send(message) for client in CONNECTED_CLIENTS])

async def handler(websocket):
    """
    Lida com cada conexão de cliente WebSocket.
    Uma instância desta função é criada para cada cliente que se conecta.
    """
    CONNECTED_CLIENTS.add(websocket)
    logging.info(f"Novo cliente conectado. Total: {len(CONNECTED_CLIENTS)}")
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                data['timestamp'] = datetime.now().strftime('%H:%M')

                log_message = f"Mensagem recebida de {data.get('user', 'desconhecido')}: {data.get('text', '')}"
                if data.get('type') == 'join':
                    log_message = f"Usuário {data.get('user', 'desconhecido')} entrou no chat."
                
                logging.info(log_message)
                
                await broadcast(json.dumps(data))

            except json.JSONDecodeError:
                logging.error(f"Erro ao decodificar JSON: {message}")
            except Exception as e:
                logging.error(f"Erro ao processar mensagem: {e}")

    finally:
        CONNECTED_CLIENTS.remove(websocket)
        logging.info(f"Cliente desconectado. Total: {len(CONNECTED_CLIENTS)}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        logging.info("✅ Servidor WebChat iniciado em ws://pychat-blhc.onrender.com")
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Servidor desligado.")