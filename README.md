# ⚡ ChargeHub - Backend

ChargeHub é uma API desenvolvida com **Python (Flask)** e **SQLite** que serve como back-end para um MVP de aplicativo de localização e agendamento de uso de estações de carregamento para veículos elétricos.

Este projeto é parte de um sistema Full Stack que permite que usuários cadastrem-se, façam login, visualizem locais disponíveis com carregadores, agendem horários e gerenciem seus compromissos.

---

## 🚀 Como executar o projeto

### ✅ Pré-requisitos

- **Python 3.11+**
- **pip** (gerenciador de pacotes do Python)

> É altamente recomendado o uso de ambiente virtual (`venv` ou `virtualenv`).

---

### 📦 Instalação e execução

1. **Clone o repositório**

```bash
git clone https://github.com/seu-usuario/chargehub-backend.git
cd chargehub-backend
```

2. **Crie e ative o ambiente virtual**.
> Windows
```bash
python -m venv venv
venv\Scripts\activate
```
>macOS/Linux
```bash
python -m venv venv
source venv/bin/activate
```
3. **Instale as dependências**
```bash
pip install -r requirements.txt
```
4. **Inicie o servidor**
```bash
python app.py
```