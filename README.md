# 💬 Pychat

## 📚 Projeto de Chat Web com Python e Sockets

Este projeto tem como objetivo implementar um chat funcional via terminal e interface web, utilizando Python no backend e tecnologias web no frontend.

---

## 👨‍💻 Desenvolvido por:

- João Pedro Rodrigue — 1134867  
- Nycolas Musskopf Fachi — 1134317

---

## 🚀 Funcionalidades

- Comunicação em tempo real entre usuários  
- Backend em Python utilizando `socket` e `threading`  
- Interface web com HTML, CSS e JavaScript  
- Interface simples e responsiva  
- Transmissão de mensagens simultâneas

---

## 🧰 Tecnologias Utilizadas

- Python 3  
- Módulos: `socket`, `threading`  
- HTML5, CSS3, JavaScript 

---

## 📂 Estrutura do Projeto

Pychat-main/
├── servidor_webchat.py # Lógica do servidor socket
├── requirements.txt # Dependências (mínimas)
└── web/
├── index.html # Estrutura da interface do chat
├── script.js # Comunicação com o servidor
└── style.css # Estilos da interface


## ⚙️ Como Executar

1. **Clone ou extraia o projeto:**

git clone https://github.com/1134867JP/Pychat.git
Ou extraia o .zip fornecido.

(Opcional) Instale os requisitos:

pip install -r requirements.txt
Observação: o projeto usa apenas bibliotecas da própria linguagem Python.

Inicie o servidor:

python servidor_webchat.py
---

Abra o arquivo index.html:

web/index.html
Use um navegador compatível. Certifique-se de que o navegador e o servidor estão no mesmo host/rede.

📝 Observações Finais
Este projeto foi desenvolvido com fins educacionais, como parte da disciplina de Computação Distribuída. Utilizamos conceitos fundamentais de rede, comunicação cliente-servidor e desenvolvimento web básico para compor a aplicação.