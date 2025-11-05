# Lista de Espera

Uma aplicação genérica de **lista de espera**, desenvolvida para ser facilmente adaptada a diferentes necessidades — seja para clínicas, restaurantes, eventos, escolas ou qualquer outro tipo de fila de atendimento.

## 🚀 Funcionalidades

- Cadastro e gerenciamento de pessoas na lista de espera  
- Atualização em tempo real (dependendo da configuração)  
- Interface simples e intuitiva
- API REST para integração com outros sistemas  
- Sistema genérico e personalizável  

## 🛠️ Tecnologias

- **Backend:** Python (Flask)  
- **Banco de Dados:** SQLite (padrão) — pode ser adaptado para MySQL, PostgreSQL, etc.  
- **Frontend:** HTML, CSS e JavaScript (Bootstrap)  
- **Containerização:** Docker (opcional)  

## ⚙️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/LuanLucasTS/lista_espera.git
   cd lista_espera
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```bash
   flask run
   ```

5. Acesse no navegador:  
   👉 [http://localhost:5000](http://localhost:5000)

## 🧩 Personalização

A estrutura da aplicação é modular, permitindo que você:
- Adicione novos campos à lista de espera  
- Altere o fluxo de entrada e saída  
- Modifique o layout da interface  
- Integre com sistemas externos via API  

## 📦 Docker

Também é possível rodar a aplicação via Docker:

```bash
docker compose up -d
```

## 🤝 Contribuições

Sinta-se à vontade para contribuir!  
Faça um *fork*, crie uma *branch*, implemente sua melhoria e envie um *pull request* 🚀

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações.

