-- Migración para crear tablas de importación masiva de visitas
CREATE TABLE IF NOT EXISTS import_headers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha_importacion DATETIME NOT NULL,
    nombre_archivo VARCHAR(255) NOT NULL,
    resumen_general VARCHAR(1024),
    FOREIGN KEY (usuario_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS import_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    import_header_id INT NOT NULL,
    linea_numero INT NOT NULL,
    nombre VARCHAR(255),
    fecha DATE,
    rating INT,
    comentarios TEXT,
    resultado VARCHAR(16),
    mensaje_error VARCHAR(512),
    FOREIGN KEY (import_header_id) REFERENCES import_headers(id)
);
