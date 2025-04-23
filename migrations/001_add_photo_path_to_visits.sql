-- Migration 001: Añadir campo photo_path a la tabla visits
ALTER TABLE visits ADD COLUMN photo_path VARCHAR(255) NULL AFTER comments;