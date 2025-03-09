# API de Ponto Eletrônico

Esta é uma API RESTful para registro e consulta de pontos eletrônicos de funcionários. Desenvolvida com Flask e Flask-RESTX, a API oferece funcionalidades para registrar pontos de entrada e saída, consultar pontos de um usuário específico, atualizar e excluir registros de ponto, além de fornecer documentação interativa usando o Swagger.

## Índice

- [Visão Geral](#visão-geral)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Uso da API](#uso-da-api)
  - [Endpoints](#endpoints)
- [Exemplos de Requisição e Resposta](#exemplos-de-requisição-e-resposta)
- [Licença](#licença)

---

## Visão Geral

Esta API permite que os administradores registrem, consultem, atualizem e excluam pontos eletrônicos de usuários, com base em suas informações (nome, e-mail, departamento, cargo, etc.). A API também oferece documentação automática utilizando o Swagger, facilitando o entendimento e o uso dos endpoints.

---

## Tecnologias Utilizadas

- **Flask** - Framework web para Python.
- **Flask-RESTX** - Extensão do Flask para criar APIs RESTful de forma simples e eficiente.
- **SQLite** - Banco de dados relacional leve utilizado para armazenamento dos registros de ponto.
- **Swagger** - Interface interativa gerada automaticamente para facilitar o uso e a documentação da API.

---

## Instalação

### Requisitos

1. **Python 3.x** - Certifique-se de ter o Python 3.x instalado em sua máquina.
2. **Dependências** - As dependências podem ser instaladas utilizando o `pip`.

### Passos para instalação:

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/ponto-eletronico-api.git
    cd ponto-eletronico-api
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Windows, use: venv\Scripts\activate
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Crie o banco de dados e as tabelas:
    O banco de dados será criado automaticamente na primeira execução da aplicação.

---

## Uso da API

### Iniciar o Servidor

Para iniciar o servidor, execute o seguinte comando:

```bash
python pontoEletronico.py
```

O servidor estará disponível em `http://localhost:5000/`.

### Acessar a Documentação Swagger

A documentação da API pode ser acessada através do Swagger na seguinte URL:

```
http://localhost:5000/
```

---

## Endpoints

Aqui estão os principais endpoints da API:

### **1. Registrar Ponto**

- **Método**: `POST`
- **Endpoint**: `/PontoEletronico/registrar_ponto`
- **Descrição**: Registra um ponto de entrada ou saída para um usuário.
  
#### Corpo da Requisição (JSON):
```json
{
  "nome": "João Silva",
  "email": "joao.silva@email.com",
  "departamento": "TI",
  "cargo": "Desenvolvedor",
  "id": "12345",
  "tipo": "entrada"
}
```

#### Resposta:
- **200 OK**: Ponto registrado com sucesso.
- **400 Bad Request**: Caso o tipo de ponto seja inválido.

---

### **2. Consultar Todos os Pontos**

- **Método**: `GET`
- **Endpoint**: `/PontoEletronico/consultar_pontos`
- **Descrição**: Retorna todos os pontos registrados no sistema.

#### Resposta:
```json
{
  "pontos": [
    {
      "usuario": {
        "nome": "João Silva",
        "email": "joao.silva@email.com",
        "departamento": "TI",
        "cargo": "Desenvolvedor",
        "id": "12345"
      },
      "tipo": "entrada",
      "hora": "09-03-2025 08:00:00"
    }
  ]
}
```

---

### **3. Consultar Pontos de um Usuário Específico**

- **Método**: `GET`
- **Endpoint**: `/PontoEletronico/consultar_pontos/<id_usuario>`
- **Descrição**: Retorna os pontos registrados de um usuário específico.

#### Parâmetro de Caminho:
- `id_usuario`: ID do usuário cujos pontos você deseja consultar.

#### Resposta:
```json
{
  "pontos": [
    {
      "usuario": {
        "nome": "João Silva",
        "email": "joao.silva@email.com",
        "departamento": "TI",
        "cargo": "Desenvolvedor",
        "id": "12345"
      },
      "tipo": "entrada",
      "hora": "09-03-2025 08:00:00"
    }
  ]
}
```

---

### **4. Atualizar um Ponto**

- **Método**: `PUT`
- **Endpoint**: `/PontoEletronico/atualizar_ponto/<ponto_id>`
- **Descrição**: Atualiza as informações de um ponto eletrônico específico.

#### Parâmetro de Caminho:
- `ponto_id`: ID do ponto que você deseja atualizar.

#### Corpo da Requisição (JSON):
```json
{
  "nome": "João Silva",
  "email": "joao.silva@email.com",
  "departamento": "TI",
  "cargo": "Desenvolvedor",
  "id": "12345",
  "tipo": "saida"
}
```

#### Resposta:
- **200 OK**: Ponto atualizado com sucesso.
- **404 Not Found**: Caso o ponto não seja encontrado.

---

### **5. Deletar um Ponto**

- **Método**: `DELETE`
- **Endpoint**: `/PontoEletronico/deletar_ponto/<ponto_id>`
- **Descrição**: Exclui um ponto eletrônico específico.

#### Parâmetro de Caminho:
- `ponto_id`: ID do ponto que você deseja excluir.

#### Resposta:
- **200 OK**: Ponto deletado com sucesso.
- **404 Not Found**: Caso o ponto não seja encontrado.

---

## Exemplos de Requisição e Resposta

### Exemplo de Requisição para Registrar Ponto

```bash
curl -X POST "http://localhost:5000/PontoEletronico/registrar_ponto" -H "Content-Type: application/json" -d '{
  "nome": "João Silva",
  "email": "joao.silva@email.com",
  "departamento": "TI",
  "cargo": "Desenvolvedor",
  "id": "12345",
  "tipo": "entrada"
}'
```

#### Exemplo de Resposta:

```json
{
  "mensagem": "Ponto de entrada registrado com sucesso!"
}
```

---

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
