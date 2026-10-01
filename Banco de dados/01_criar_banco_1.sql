/* ============================================================
   Projeto Nora - Assistente por voz
   Script 1 de 3: criação do banco e das tabelas
   Banco: SQL Server (T-SQL)
   ============================================================ */

-- Cria o banco de dados (rode esta parte uma vez só)
CREATE DATABASE nora;
GO

-- Entra no banco nora para os comandos seguintes
USE nora;
GO

/* ------------------------------------------------------------
   Tabela: tarefas
   ------------------------------------------------------------ */
CREATE TABLE tarefas (
    id          INT           IDENTITY(1,1) PRIMARY KEY,
    titulo      NVARCHAR(200) NOT NULL,
    concluida   BIT           NOT NULL DEFAULT 0,
    prioridade  NVARCHAR(10)  NOT NULL DEFAULT 'media',
    criada_em   DATETIME2     NOT NULL DEFAULT SYSDATETIME()
);
GO

/* ------------------------------------------------------------
   Tabela: notas
   ------------------------------------------------------------ */
CREATE TABLE notas (
    id         INT           IDENTITY(1,1) PRIMARY KEY,
    conteudo   NVARCHAR(MAX) NOT NULL,
    criada_em  DATETIME2     NOT NULL DEFAULT SYSDATETIME()
);
GO

/* ------------------------------------------------------------
   Tabela: compromissos
   ------------------------------------------------------------ */
CREATE TABLE compromissos (
    id          INT           IDENTITY(1,1) PRIMARY KEY,
    titulo      NVARCHAR(200) NOT NULL,
    data_hora   DATETIME2     NOT NULL,
    local       NVARCHAR(200) NULL,          -- opcional
    criada_em   DATETIME2     NOT NULL DEFAULT SYSDATETIME()
);
GO

/* ------------------------------------------------------------
   Tabela: categorias  (para organizar as tarefas)
   ------------------------------------------------------------ */
CREATE TABLE categorias (
    id    INT          IDENTITY(1,1) PRIMARY KEY,
    nome  NVARCHAR(50) NOT NULL
);
GO

/* ------------------------------------------------------------
   Liga tarefas a categorias (chave estrangeira).
   categoria_id aponta para categorias.id; NULL = tarefa sem categoria.
   ------------------------------------------------------------ */
ALTER TABLE tarefas
ADD categoria_id INT NULL
    FOREIGN KEY REFERENCES categorias(id);
GO
