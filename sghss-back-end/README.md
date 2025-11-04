# SGHSS - Sistema de Gestão Hospitalar e de Serviços de Saúde

Projeto desenvolvido como atividade prática da disciplina de Projeto Multidisciplinar - UNINTER (ênfase em Back-end).

## Objetivo

Desenvolver um sistema teórico com protótipo funcional para gestão hospitalar, incluindo:
- Cadastro de pacientes e profissionais
- Agendamento de consultas e teleconsultas
- Emissão de receitas digitais
- Registro de prontuários
- Controle de leitos, suprimentos e financeiro
- Segurança de dados conforme LGPD

## Tecnologias Utilizadas

- Python 3.11
- Flask
- MySQL
- SQLAlchemy
- JWT (JSON Web Token)
- Bcrypt
- GitHub (controle de versão)

## Segurança

- Autenticação via JWT
- Criptografia de senhas com bcrypt
- Controle de acesso por perfil (admin, profissional, paciente)
- Registro de auditoria para rastreabilidade

## Requisitos

- Python 3.11+
- MySQL Server
- pip (gerenciador de pacotes)

## Funcionalidades
- Cadastro e gerenciamento de pacientes
- Agendamento de consultas e teleconsultas
- Emissão de receitas digitais
- Atualização de prontuários médicos
- Controle de profissionais e usuários
- Gestão de leitos hospitalares
- Administração de suprimentos e financeiro
- Registro de auditoria de ações

## Exemplos de Requisições
- POST /usuarios → cadastro de usuário
- POST /login → autenticação e retorno de token JWT
- GET /pacientes → listagem autenticada
- POST /consultas → agendamento de consulta
- PUT /consultas/{id} → atualização de consulta
- DELETE /consultas/{id} → exclusão de consulta

## Repositório
Este projeto está disponível em:
🔗 github.com/gabspo/sghss-back-end

## Autor
Gabriel Sponton Beretta
RU: 4573718


