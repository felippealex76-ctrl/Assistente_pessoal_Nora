-- ============================================================
--  Nora — criação do banco e das tabelas (SQL Server / T-SQL)
--  Rode este script no SQL Server Management Studio (SSMS).
-- ============================================================

-- Cria o banco (se ainda não existir)
IF DB_ID('nora') IS NULL
    CREATE DATABASE nora;
GO

USE nora;
GO

-- Tarefas -----------------------------------------------------
IF OBJECT_ID('tarefas', 'U') IS NULL
CREATE TABLE tarefas (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    titulo      NVARCHAR(200) NOT NULL,
    prioridade  NVARCHAR(10)  NOT NULL DEFAULT 'media',   -- alta | media | baixa
    concluida   BIT           NOT NULL DEFAULT 0
);
GO

-- Notas -------------------------------------------------------
IF OBJECT_ID('notas', 'U') IS NULL
CREATE TABLE notas (
    id         INT IDENTITY(1,1) PRIMARY KEY,
    conteudo   NVARCHAR(MAX) NOT NULL,
    criada_em  DATETIME2     NOT NULL DEFAULT SYSDATETIME()
);
GO

-- Compromissos ------------------------------------------------
IF OBJECT_ID('compromissos', 'U') IS NULL
CREATE TABLE compromissos (
    id         INT IDENTITY(1,1) PRIMARY KEY,
    titulo     NVARCHAR(200) NOT NULL,
    data_hora  DATETIME2     NOT NULL,
    local      NVARCHAR(200) NULL
);
GO
