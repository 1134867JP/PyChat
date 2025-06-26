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
    
    user_name = None
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                data['timestamp'] = datetime.now().strftime('%H:%M')

                if data.get('type') == 'join':
                    user_name = data.get('user', 'desconhecido')
                    log_message = f"Usuário {user_name} entrou no chat."
                else:
                    log_message = f"Mensagem recebida de {data.get('user', 'desconhecido')}: {data.get('text', '')}"
                
                logging.info(log_message)
                
                await broadcast(json.dumps(data))

            except json.JSONDecodeError:
                logging.error(f"Erro ao decodificar JSON: {message}")
            except Exception as e:
                logging.error(f"Erro ao processar mensagem: {e}")

    finally:
        CONNECTED_CLIENTS.remove(websocket)
        if user_name:
            leave_message = {
                'type': 'leave',
                'user': user_name,
                'timestamp': datetime.now().strftime('%H:%M')
            }
            await broadcast(json.dumps(leave_message))
            logging.info(f"Usuário {user_name} saiu do chat. Total: {len(CONNECTED_CLIENTS)}")
        else:
            logging.info(f"Cliente desconectado (sem nome de usuário). Total: {len(CONNECTED_CLIENTS)}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        logging.info("✅ Servidor WebChat iniciado em ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Servidor desligado.")