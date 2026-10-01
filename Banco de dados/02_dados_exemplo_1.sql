/* ============================================================
   Projeto Nora
   Script 2 de 3: dados de exemplo
   Rode depois do 01_criar_banco.sql
   ============================================================ */

USE nora;
GO

-- Categorias (crie antes das tarefas, para poder ligá-las)
INSERT INTO categorias (nome) VALUES
('Trabalho'),
('Estudos'),
('Pessoal');
GO

-- Tarefas
INSERT INTO tarefas (titulo, prioridade) VALUES
('Estudar SQL', 'alta'),
('Comprar pão', 'baixa'),
('Ligar para o dentista', 'media'),
('Terminar o projeto Nora', 'alta');
GO

-- Liga algumas tarefas às categorias.
-- (confira os ids com: SELECT * FROM categorias;  e  SELECT * FROM tarefas;)
UPDATE tarefas SET categoria_id = 2 WHERE titulo = 'Estudar SQL';            -- Estudos
UPDATE tarefas SET categoria_id = 1 WHERE titulo = 'Terminar o projeto Nora'; -- Trabalho
UPDATE tarefas SET categoria_id = 3 WHERE titulo = 'Comprar pão';            -- Pessoal
GO

-- Notas
INSERT INTO notas (conteudo) VALUES
('Lembrar de revisar os conceitos de JOIN'),
('Ideia: a Nora poderia dar bom dia com a previsão do tempo'),
('Senha do wi-fi do escritório fica com o suporte');
GO

-- Compromissos
INSERT INTO compromissos (titulo, data_hora, local) VALUES
('Reunião de equipe', '2026-10-05 14:30:00', 'Sala 3'),
('Consulta no dentista', '2026-10-08 09:00:00', NULL);
GO
