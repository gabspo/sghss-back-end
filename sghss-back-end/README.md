# sghss-back-end
# SGHSS - Sistema de Gestão Hospitalar e de Serviços de Saúde

Projeto desenvolvido como atividade prática da disciplina de Projeto Multidisciplinar - UNINTER (ênfase em Back-end).

## Objetivo
Desenvolver um sistema teórico com protótipo funcional para gestão hospitalar, incluindo cadastro de pacientes, profissionais, telemedicina e segurança de dados.

## Tecnologias Utilizadas
- Python 3.11
- Flask
- MySQL
- SQLAlchemy
- JWT (JSON Web Token)
- GitHub (controle de versão)

## Estrutura do Projeto
- src/ ├── controllers/ ├── models/ ├── routes/ ├── services/ ├── utils/ ├── config.py ├── app.py tests/ README.md requirements.txt


## Segurança
- Autenticação via JWT
- Criptografia de senhas com bcrypt
- Controle de acesso por perfil

## Requisitos
- Python 3.11+
- MySQL Server
- pip (gerenciador de pacotes)

## Execução
```bash
pip install -r requirements.txt
python src/app.py