-- Índices adicionales para optimizar búsquedas (Tema 12)
-- Ejecutar después de crear las tablas

-- Índices para alumnos
CREATE INDEX IF NOT EXISTS idx_alumnos_dni ON alumnos(dni);

-- Índices para profesores
CREATE INDEX IF NOT EXISTS idx_profesores_dni ON profesores(dni);

-- Índices para la vista (si es posible indexar vistas materializadas)
-- Nota: Las vistas normales no se pueden indexar directamente,
-- pero las tablas base ya tienen índices que ayudan