# ProjetoJanela_IOT
# 🪟 Janela Inteligente IoT

> Sistema IoT para automação de janelas baseado em condições ambientais, utilizando ESP32, sensores, MQTT, backend Flask e interface web moderna.

Este projeto implementa um sistema de automação para abertura e fechamento de uma janela com base em variáveis ambientais (temperatura, umidade, chuva e luminosidade). Utiliza ESP32, sensores ambientais e um servo motor, com integração via MQTT e backend Flask com painel web.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Componentes Utilizados](#componentes-utilizados)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração e Execução](#configuração-e-execução)
- [Lógica do Modo Automático](#lógica-do-modo-automático)
- [Fluxo de Comunicação](#fluxo-de-comunicação)
- [Capturas de Tela](#capturas-de-tela)
- [Contribuições](#contribuições)

## 🔍 Visão Geral

A Janela Inteligente IoT é uma solução que automatiza o controle de ventilação e iluminação natural em ambientes residenciais e comerciais. O sistema monitora continuamente as condições climáticas e controla automaticamente a abertura e fechamento da janela, proporcionando maior conforto térmico, economia de energia e proteção contra intempéries.

![Conceito da Janela Inteligente](imagens/janela_inteligente_conceito.png)

## 📦 Funcionalidades

- Monitoramento de:
  - 🌡️ Temperatura (DHT22)
  - 💧 Umidade relativa do ar
  - 🌧️ Detecção de chuva (push-button)
  - ☀️ Luminosidade (LDR)
- Controle manual da janela via interface web (Abrir / Fechar)
- Modo automático: atuações baseadas em lógica climática
- Backend Python Flask que:
  - Recebe comandos da interface web
  - Publica comandos via MQTT
  - Recebe dados do ESP32 via MQTT
- Interface web com visual moderno usando TailwindCSS e Font Awesome

## 🧰 Componentes Utilizados

| Componente         | Função                             |
|--------------------|------------------------------------|
| ESP32              | Microcontrolador principal         |
| DHT22              | Sensor de temperatura e umidade    |
| Push-button        | Simulação de sensor de chuva       |
| LDR + Resistor     | Sensor de luminosidade             |
| Servo Motor        | Abertura e fechamento da janela    |
| Flask (Python)     | Backend HTTP + MQTT                |
| Paho MQTT          | Comunicação MQTT entre ESP e Backend |
| TailwindCSS        | Estilo da interface web            |
| Font Awesome       | Ícones para a interface web        |

## 📁 Estrutura do Projeto

```
janela_inteligente_iot/
├── codigo/
│   ├── microcontrolador_code.cpp  # Código C++ para ESP32 (Wokwi)
│   ├── backend_code.py            # Backend Python Flask com MQTT
│   └── interface_app.html         # Interface web com TailwindCSS
├── documentacao/
│   ├── documentacao_completa.md   # Documentação detalhada em Markdown
│   └── documentacao_janela_inteligente.pdf  # Documentação em PDF
├── imagens/
│   ├── janela_inteligente_conceito.png  # Imagem conceitual do projeto
│   └── diagrama_arquitetura.png         # Diagrama de arquitetura do sistema
└── apresentacao/                  # Slides de apresentação do projeto
```

## ⚙️ Configuração e Execução

### 1. Simulação do Microcontrolador (ESP32) no Wokwi

1. Acesse o [Wokwi](https://wokwi.com/)
2. Crie um novo projeto ESP32
3. Configure os componentes conforme a tabela abaixo:

| Componente     | GPIO (Pino) |
|----------------|-------------|
| DHT22          | GPIO 4      |
| Push-button    | GPIO 19     |
| LDR            | GPIO 34     |
| Servo Motor    | GPIO 22     |

4. Cole o código do arquivo `codigo/microcontrolador_code.cpp` no editor
5. Inicie a simulação clicando no botão "Play"

### 2. Backend Python (Flask)

1. Instale as dependências:
```bash
pip install flask flask-cors paho-mqtt
```

2. Execute o backend:
```bash
python codigo/backend_code.py
```

O servidor Flask iniciará em `http://127.0.0.1:5000`

### 3. Interface Web

1. Abra o arquivo `codigo/interface_app.html` no seu navegador
2. A interface se conectará automaticamente ao backend Flask

## 🧠 Lógica do Modo Automático

O sistema implementa a seguinte lógica quando o modo automático está ativado:

- **Abrir janela automaticamente** se temperatura > 28°C
- **Fechar janela** se:
  - Está chovendo (botão pressionado)
  - Temperatura < 25°C
- Modo manual sempre sobrepõe temporariamente o modo automático

## 🔄 Fluxo de Comunicação

![Diagrama de Arquitetura](imagens/diagrama_arquitetura.png)

O sistema funciona com o seguinte fluxo de comunicação:

1. **ESP32 (Wokwi)** lê os sensores e publica os dados no tópico MQTT `janela/dados`
2. **Backend Flask** recebe os dados via MQTT e atualiza seu estado interno
3. **Interface Web** solicita o status atual ao backend via HTTP GET
4. **Interface Web** envia comandos ao backend via HTTP POST
5. **Backend Flask** recebe comandos da interface e os publica no tópico MQTT `janela/comando`
6. **ESP32 (Wokwi)** recebe os comandos via MQTT e executa as ações correspondentes

## 📸 Capturas de Tela

A interface web da Janela Inteligente IoT apresenta um design moderno e responsivo:

- Visualização em tempo real dos dados dos sensores
- Controle manual da janela (abrir/fechar)
- Ativação/desativação do modo automático
- Status visual da janela (aberta/fechada)

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorar este projeto.

---

Desenvolvido como projeto educacional para demonstração de conceitos de IoT, programação e conectividade.
