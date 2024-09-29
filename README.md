# Python-Projeto_integrador
 API de Gerenciamento de Usuários, Armazenamento e Produtos
Introdução

Esta API, desenvolvida com Flask e MySQL, oferece funcionalidades para gerenciar usuários, locais de armazenamento e produtos. A API inclui autenticação, controle de permissões e limite de requisições por minuto para garantir segurança e eficiência.
Endpoints Disponíveis

    Login
    Cadastro de Usuários
    Consulta e Atualização de Usuários
    Cadastro de Armazenamento
    Consulta e Atualização de Armazenamento
    Cadastro de Produtos
    Consulta e Atualização de Produtos

Configurações Gerais

    Porta: 3000
    Host: 0.0.0.0
    Limite de Requisições: 5 requisições por minuto em todos os endpoints.

1. Login
Rota: /api/validar_login

    Método HTTP: POST
    Descrição: Valida o login de um usuário.

Requisição:

json

{
  "usuario": "nome_do_usuario",
  "senha": "senha_do_usuario"
}

Resposta:

    200 OK: Login bem-sucedido

    json

{
  "status": true,
  "aut": valor_autorizacao
}

401 Unauthorized: Login inválido

json

{
  "status": false,
  "aut": 0
}

400 Bad Request: Parâmetros inválidos

json

    {
      "status": false,
      "aut": 0
    }

2. Cadastro de Usuário
Rota: /api/cadastro_usuario

    Método HTTP: POST
    Descrição: Cadastra um novo usuário. Apenas usuários com autorização nível 5 podem realizar essa operação.

Requisição:

json

{
  "aut_usuario": 5,
  "usuario": "novo_usuario",
  "senha": "nova_senha",
  "aut": 3
}

Resposta:

    201 Created: Usuário cadastrado

    json

{
  "status": true
}

403 Forbidden: Permissão negada

json

{
  "status": false,
  "message": "Permissão negada"
}

400 Bad Request: Campos obrigatórios faltantes

json

    {
      "status": false,
      "message": "Todos os campos são obrigatórios"
    }

3. Atualização de Usuário
Rota: /api/update_usuario

    Método HTTP: PUT
    Descrição: Atualiza as informações de um usuário.

Requisição:

json

{
  "cod": 1,
  "usuario": "usuario_atualizado",
  "senha": "senha_atualizada",
  "aut": 3
}

Resposta:

    200 OK: Usuário atualizado

    json

{
  "status": true,
  "message": "Usuário atualizado com sucesso"
}

404 Not Found: Usuário não encontrado

json

{
  "status": false,
  "message": "Usuário não encontrado"
}

400 Bad Request: Campos obrigatórios faltantes

json

    {
      "status": false,
      "message": "Todos os campos são obrigatórios"
    }

4. Consulta de Usuários
Rota: /api/consulta_usuarios

    Método HTTP: GET
    Descrição: Consulta todos os usuários. Apenas usuários com autorização 5 podem acessar.

Resposta:

    200 OK: Lista de usuários

    json

[
  {
    "cod": 1,
    "usuario": "usuario1",
    "senha": "senha1",
    "aut": 5
  },
  {
    "cod": 2,
    "usuario": "usuario2",
    "senha": "senha2",
    "aut": 3
  }
]

403 Forbidden: Permissão negada

json

    {
      "status": false,
      "message": "Permissão negada"
    }

5. Cadastro de Armazenamento
Rota: /api/cadastro_armazenamento

    Método HTTP: POST
    Descrição: Cadastra um novo local de armazenamento.

Requisição:

json

{
  "desc_local": "Novo Local"
}

Resposta:

    201 Created: Local cadastrado

    json

{
  "status": true
}

400 Bad Request: Parâmetro obrigatório faltante

json

    {
      "status": false
    }

6. Consulta de Armazenamento
Rota: /api/consulta_armazenamento

    Método HTTP: GET
    Descrição: Consulta todos os locais de armazenamento.

Resposta:

    200 OK: Lista de locais

    json

[
  {
    "cod": 1,
    "desc_local": "Local 1"
  },
  {
    "cod": 2,
    "desc_local": "Local 2"
  }
]

500 Internal Server Error: Erro no banco de dados

json

    {
      "status": false,
      "message": "Erro no banco de dados"
    }

7. Atualização de Armazenamento
Rota: /api/update_armazenamento

    Método HTTP: PUT
    Descrição: Atualiza as informações de um local de armazenamento.

Requisição:

json

{
  "cod": 1,
  "desc_local": "Local Atualizado"
}

Resposta:

    200 OK: Armazenamento atualizado

    json

{
  "status": true,
  "message": "Armazenamento atualizado com sucesso"
}

404 Not Found: Local não encontrado

json

{
  "status": false,
  "message": "Código do armazenamento não encontrado"
}

400 Bad Request: Parâmetros inválidos

json

    {
      "status": false,
      "message": "Os campos 'cod' e 'desc_local' são obrigatórios"
    }

8. Cadastro de Produto
Rota: /api/cadastro_produto

    Método HTTP: POST
    Descrição: Cadastra um novo produto.

Requisição:

json

{
  "codArmaz": 1,
  "dscNome": "Produto 1",
  "fornecedor": "Fornecedor X",
  "qtdMaxima": 100,
  "estadoFisico": "Líquido",
  "substancias": "Substância Y",
  "numeroCas": "123-45-6",
  "concentracao": "10%",
  "classsGHS": "Classe GHS 1",
  "elemento1": "Elemento 1",
  "elemento2": "Elemento 2",
  "elemento3": "Elemento 3",
  "advertencia": "Advertência",
  "frasePerigo": "Frase de Perigo",
  "frasePrecaucao": "Frase de Precaução"
}

Resposta:

    201 Created: Produto cadastrado

    json

{
  "status": true
}

400 Bad Request: Parâmetros faltantes

json

    {
      "status": false,
      "message": "O campo 'campo_faltante' é obrigatório"
    }

9. Consulta de Produto
Rota: /api/consulta_produto

    Método HTTP: GET
    Descrição: Consulta todos os produtos ou um produto específico.

Parâmetro de URL:

    cod: Código do produto (opcional).

Resposta:

    200 OK: Produto(s) encontrado(s)

    json

[
  {
    "cod": 1,
    "dscNome": "Produto 1",
    "fornecedor": "Fornecedor X",
    ...
  }
]

404 Not Found: Produto não encontrado

json

    {
      "status": false,
      "message": "Produto não encontrado"
    }

10. Atualização de Produto
Rota: /api/update_produto

    Método HTTP: PUT
    Descrição: Atualiza as informações de um produto existente.

Requisição:

json

{
  "cod": 1,
  "dscNome": "Produto Atualizado",
  "fornecedor": "Fornecedor Y",
  ...
}

Resposta:

    200 OK: Produto atualizado com sucesso

    json

{
  "status": true,
  "message": "Produto atualizado com sucesso"
}

404 Not Found: Produto não encontrado

json

{
  "status": false,
  "message": "Código do produto não encontrado"
}

400 Bad Request: Falta de parâmetros obrigatórios

json

    {
      "status": false,
      "message": "Os campos obrigatórios são 'cod' e 'dscNome'"
    }

Conclusão

Essa API permite o gerenciamento completo de usuários, locais de armazenamento e produtos. Todos os endpoints são protegidos por um limite de requisições por minuto, e os acessos são registrados para auditoria e monitoramento.

