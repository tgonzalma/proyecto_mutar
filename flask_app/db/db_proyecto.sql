ALTER TABLE eventos 
MODIFY COLUMN latitud DECIMAL(9,6) NULL,
MODIFY COLUMN longitud DECIMAL(9,6) NULL;

-- Agregar columna para foto de portada
ALTER TABLE eventos 
ADD COLUMN foto_portada VARCHAR(255) NULL AFTER estado;

-- Agregar columna para foto de portada en grupos
ALTER TABLE grupos 
ADD COLUMN foto_portada VARCHAR(255) NULL AFTER descripcion;