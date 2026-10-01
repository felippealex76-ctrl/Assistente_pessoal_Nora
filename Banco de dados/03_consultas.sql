/* ============================================================
   Projeto Nora
   Script 3 de 3: consultas de exemplo
   Coleção dos SELECTs que aprendemos. Rode à vontade; não altera dados.
   ============================================================ */

USE nora;
GO

-- Todas as tarefas
SELECT * FROM tarefas;
GO

-- Só título e prioridade
SELECT titulo, prioridade FROM tarefas;
GO

-- Filtrar: tarefas pendentes de prioridade alta
SELECT * FROM tarefas
WHERE concluida = 0 AND prioridade = 'alta';
GO

-- Ordenar: compromissos pela data, o próximo primeiro
SELECT titulo, data_hora, local
FROM compromissos
ORDER BY data_hora ASC;
GO

/* ------------------------------------------------------------
   JOIN: tarefa + nome da categoria
   INNER JOIN -> só tarefas que TÊM categoria
   ------------------------------------------------------------ */
SELECT t.titulo, t.prioridade, c.nome AS categoria
FROM tarefas t
INNER JOIN categorias c ON t.categoria_id = c.id;
GO

/* ------------------------------------------------------------
   LEFT JOIN: TODAS as tarefas, com ou sem categoria
   (as sem categoria aparecem com NULL em "categoria")
   ------------------------------------------------------------ */
SELECT t.titulo, t.prioridade, c.nome AS categoria
FROM tarefas t
LEFT JOIN categorias c ON t.categoria_id = c.id;
GO
