-- ============================================================================
-- SCRIPT DE INICIALIZAÇÃO DO BANCO DE DADOS SGHSS
-- Sistema de Gestão de Saúde e Segurança em Telemedicina
-- ============================================================================

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS sghss_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Selecionar banco de dados
USE sghss_db;

-- ============================================================================
-- TABELA: usuarios
-- Descrição: Todos os usuários do sistema (admin, médico, paciente, secretária)
-- ============================================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'medico', 'paciente', 'secretaria') NOT NULL DEFAULT 'paciente',
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_tipo (tipo),
    INDEX idx_ativo (ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABELA: pacientes
-- Descrição: Informações específicas de pacientes
-- Relacionamento: FK para usuarios (1-para-1)
-- ============================================================================
CREATE TABLE IF NOT EXISTS pacientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL UNIQUE,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE,
    telefone VARCHAR(20),
    endereco VARCHAR(500),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    cep VARCHAR(9),
    condicoes_medicas TEXT,
    alergias TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_pacientes_usuarios FOREIGN KEY (usuario_id) 
        REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE,
    
    INDEX idx_cpf (cpf),
    INDEX idx_usuario_id (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABELA: profissionais
-- Descrição: Informações de médicos e outros profissionais de saúde
-- Relacionamento: FK para usuarios (1-para-1)
-- ============================================================================
CREATE TABLE IF NOT EXISTS profissionais (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL UNIQUE,
    crm VARCHAR(20) UNIQUE NOT NULL,
    especialidade VARCHAR(100) NOT NULL,
    telefone_comercial VARCHAR(20),
    endereco_consultorio VARCHAR(500),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    cep VARCHAR(9),
    horario_inicio TIME,
    horario_fim TIME,
    dias_atendimento VARCHAR(100),
    biografia TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_profissionais_usuarios FOREIGN KEY (usuario_id) 
        REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE,
    
    INDEX idx_crm (crm),
    INDEX idx_especialidade (especialidade),
    INDEX idx_usuario_id (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABELA: medicamentos
-- Descrição: Catálogo de medicamentos disponíveis no sistema
-- Relacionamento: Nenhum (tabela independente)
-- ============================================================================
CREATE TABLE IF NOT EXISTS medicamentos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    principio_ativo VARCHAR(255) NOT NULL,
    fabricante VARCHAR(255),
    dosagem VARCHAR(100),
    forma_farmaceutica VARCHAR(100),
    lote VARCHAR(50),
    validade DATE,
    preco DECIMAL(10, 2),
    estoque INT DEFAULT 0,
    descricao TEXT,
    contraindicacoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_nome (nome),
    INDEX idx_principio_ativo (principio_ativo),
    INDEX idx_lote (lote)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABELA: consultas
-- Descrição: Agendamentos e registros de consultas/atendimentos
-- Relacionamento: FK para pacientes, profissionais
-- ============================================================================
CREATE TABLE IF NOT EXISTS consultas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT NOT NULL,
    profissional_id INT NOT NULL,
    tipo ENUM('presencial', 'telemedicina') NOT NULL DEFAULT 'presencial',
    data_hora DATETIME NOT NULL,
    duracao_minutos INT DEFAULT 30,
    motivo_consulta VARCHAR(500),
    sintomas TEXT,
    diagnostico TEXT,
    observacoes TEXT,
    link_video VARCHAR(500),
    status ENUM('agendada', 'realizada', 'cancelada', 'nao_compareceu') NOT NULL DEFAULT 'agendada',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_consultas_pacientes FOREIGN KEY (paciente_id) 
        REFERENCES pacientes(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_consultas_profissionais FOREIGN KEY (profissional_id) 
        REFERENCES profissionais(id) ON DELETE CASCADE ON UPDATE CASCADE,
    
    INDEX idx_paciente_id (paciente_id),
    INDEX idx_profissional_id (profissional_id),
    INDEX idx_data_hora (data_hora),
    INDEX idx_status (status),
    INDEX idx_tipo (tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABELA: prescricoes
-- Descrição: Prescrições de medicamentos para pacientes
-- Relacionamento: FK para consultas, medicamentos, profissionais
-- ============================================================================
CREATE TABLE IF NOT EXISTS prescricoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    consulta_id INT NOT NULL,
    medicamento_id INT NOT NULL,
    profissional_id INT NOT NULL,
    dosagem VARCHAR(100) NOT NULL,
    frequencia VARCHAR(100) NOT NULL,
    duracao_dias INT NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    instrucoes_uso TEXT,
    observacoes TEXT,
    ativa BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_prescricoes_consultas FOREIGN KEY (consulta_id) 
        REFERENCES consultas(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_prescricoes_medicamentos FOREIGN KEY (medicamento_id) 
        REFERENCES medicamentos(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_prescricoes_profissionais FOREIGN KEY (profissional_id) 
        REFERENCES profissionais(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    
    INDEX idx_consulta_id (consulta_id),
    INDEX idx_medicamento_id (medicamento_id),
    INDEX idx_profissional_id (profissional_id),
    INDEX idx_ativa (ativa),
    INDEX idx_data_inicio (data_inicio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- INSERÇÕES DE TESTE (OPCIONAL)
-- ============================================================================

-- Usuário Admin
INSERT INTO usuarios (nome, email, senha, tipo, ativo) 
VALUES ('Admin Sistema', 'admin@sghss.com', 'hashed_password_admin', 'admin', TRUE);

-- Usuário Médico
INSERT INTO usuarios (nome, email, senha, tipo, ativo) 
VALUES ('Dr. João Silva', 'joao@sghss.com', 'hashed_password_medico', 'medico', TRUE);

-- Usuário Paciente
INSERT INTO usuarios (nome, email, senha, tipo, ativo) 
VALUES ('Maria Santos', 'maria@example.com', 'hashed_password_paciente', 'paciente', TRUE);

-- Profissional (associado ao usuário médico)
INSERT INTO profissionais (usuario_id, crm, especialidade, telefone_comercial, 
                          endereco_consultorio, cidade, estado, cep, 
                          horario_inicio, horario_fim, dias_atendimento)
VALUES (2, '123456/SP', 'Cardiologia', '(11) 98765-4321', 
        'Rua das Flores, 123', 'São Paulo', 'SP', '01234-567',
        '08:00:00', '18:00:00', 'Segunda a Sexta');

-- Paciente (associado ao usuário paciente)
INSERT INTO pacientes (usuario_id, cpf, data_nascimento, telefone, 
                       endereco, cidade, estado, cep)
VALUES (3, '12345678901234', '1990-05-15', '(11) 99876-5432',
        'Avenida Paulista, 1000', 'São Paulo', 'SP', '01311-100');

-- Medicamentos
INSERT INTO medicamentos (nome, principio_ativo, fabricante, dosagem, 
                         forma_farmaceutica, estoque, preco)
VALUES 
('Dipirona', 'Metamizol', 'Blau', '500mg', 'Comprimido', 100, 15.50),
('Amoxicilina', 'Amoxicilina', 'EMS', '500mg', 'Comprimido', 50, 25.00),
('Omeprazol', 'Omeprazol', 'Medley', '20mg', 'Cápsula', 75, 35.00);

-- ============================================================================
-- RELATÓRIOS DE VERIFICAÇÃO
-- ============================================================================

-- Verificar tabelas criadas
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'sghss_db';

-- Verificar usuários criados
SELECT id, nome, email, tipo FROM usuarios;

-- Verificar relacionamentos
SELECT 'Pacientes' as entity, COUNT(*) as total FROM pacientes
UNION ALL
SELECT 'Profissionais', COUNT(*) FROM profissionais
UNION ALL
SELECT 'Medicamentos', COUNT(*) FROM medicamentos
UNION ALL
SELECT 'Usuários', COUNT(*) FROM usuarios;

-- ============================================================================
-- FIM DO SCRIPT
-- ============================================================================
