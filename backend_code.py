from flask import Flask, request, jsonify
from flask_cors import CORS

import json
import paho.mqtt.client as mqtt
import time
import threading

app = Flask(__name__)
CORS(app) # Habilita CORS para todas as rotas


# Simula um banco de dados para armazenar o estado da janela
window_state = {
    "temperatura": 25.0,
    "umidade": 60.0,
    "chovendo": False,
    "luminosidade": 500.0,
    "status_janela": "fechada",
    "modo_automatico": False  
}

# Configurações MQTT
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC_DATA = "janela/dados" # Onde o microcontrolador publica dados
MQTT_TOPIC_COMMAND = "janela/comando" # Onde o backend publica comandos

# Callback quando o cliente MQTT se conecta ao broker
def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker MQTT com código de resultado {rc}")
    # Se inscreve nos tópicos que o microcontrolador publica
    client.subscribe(MQTT_TOPIC_DATA)

# Callback quando uma mensagem MQTT é recebida
def on_message(client, userdata, msg):
    global window_state
    print(f"Mensagem MQTT recebida no tópico {msg.topic}: {msg.payload.decode()}")
    if msg.topic == MQTT_TOPIC_DATA:
        try:
            data = json.loads(msg.payload.decode())
            window_state.update(data)
            print(f"Estado da janela atualizado via MQTT: {window_state}")
        except json.JSONDecodeError:
            print("Erro ao decodificar JSON da mensagem MQTT.")

# Cria um cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Função para iniciar o cliente MQTT em uma thread separada
def mqtt_loop_start():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever() # Mantém a conexão e processa mensagens

# Inicia o cliente MQTT em uma thread separada para não bloquear o Flask
mqtt_thread = threading.Thread(target=mqtt_loop_start)
mqtt_thread.daemon = True # Permite que a thread seja encerrada com o programa principal
mqtt_thread.start()


@app.route("/janela/dados", methods=["POST"])
def receive_data_http( ):
    # Este endpoint HTTP pode ser mantido para compatibilidade ou removido se tudo for via MQTT
    global window_state
    data = request.get_json()
    if data:
        window_state.update(data)
        print(f"Dados recebidos via HTTP: {window_state}")
        return jsonify({"message": "Dados recebidos com sucesso"}), 200
    return jsonify({"error": "Nenhum dado recebido"}), 400

@app.route("/janela/comando", methods=["POST"])
def send_command_http():
    global window_state
    command = request.get_json()
    if command and "acao" in command:
        acao = command["acao"]
        
        if acao == "abrir":
            window_state["status_janela"] = "aberta"
            print(f"Comando '{acao}' recebido via HTTP. Publicando via MQTT...")
            mqtt_client.publish(MQTT_TOPIC_COMMAND, acao)
            return jsonify({"message": "Comando 'abrir' enviado com sucesso"}), 200
        
        elif acao == "fechar":
            window_state["status_janela"] = "fechada"
            print(f"Comando '{acao}' recebido via HTTP. Publicando via MQTT...")
            mqtt_client.publish(MQTT_TOPIC_COMMAND, acao)
            return jsonify({"message": "Comando 'fechar' enviado com sucesso"}), 200
        
        elif acao == "ativar_automatico":
            window_state["modo_automatico"] = True
            print("Modo automático ativado.")
            mqtt_client.publish(MQTT_TOPIC_COMMAND, acao)
            return jsonify({"message": "Modo automático ativado"}), 200
        
        elif acao == "desativar_automatico":
            window_state["modo_automatico"] = False
            print("Modo automático desativado.")
            mqtt_client.publish(MQTT_TOPIC_COMMAND, acao)
            return jsonify({"message": "Modo automático desativado"}), 200

        else:
            return jsonify({"error": "Ação inválida"}), 400

    return jsonify({"error": "Nenhum comando recebido"}), 400


@app.route("/janela/status", methods=["GET"])
def get_status():
    return jsonify(window_state), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
