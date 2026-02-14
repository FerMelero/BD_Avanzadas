# Conectarse a la base de datos
+ Configurar database.ini
+ Ejecutar python connect.py
# Crear tablas en la base de datos
+ Ejecutar python create_tables.py
# Insertar valores
+ python insert.py
# Actualizar valores 
+ python update.py
# Transacciones
+ python transaction.py
# Query data
+ python query.py
# Funciones SQL
Con PSQL creamos la función

CREATE OR REPLACE FUNCTION get_parts_by_vendor(id INTEGER)
  RETURNS TABLE(part_id INTEGER, part_name VARCHAR) AS
$$
BEGIN
 RETURN QUERY

 SELECT parts.part_id, parts.part_name
 FROM parts
 INNER JOIN vendor_parts on vendor_parts.part_id = parts.part_id
 WHERE vendor_id = id;

END; $$

LANGUAGE plpgsql;

+ python get_parts_by_vendor.py

# Creamos procedimientos

CREATE OR REPLACE PROCEDURE add_new_part(
	new_part_name varchar,
	new_vendor_name varchar
) 
AS $$
DECLARE
	v_part_id INT;
	v_vendor_id INT;
BEGIN
	-- insert into the parts table
	INSERT INTO parts(part_name) 
	VALUES(new_part_name) 
	RETURNING part_id INTO v_part_id;
	
	-- insert a new vendor
	INSERT INTO vendors(vendor_name)
	VALUES(new_vendor_name)
	RETURNING vendor_id INTO v_vendor_id;
	
	-- insert into vendor_parts
	INSERT INTO vendor_parts(part_id, vendor_id)
	VALUEs(v_part_id,v_vendor_id);
	
END;
$$
LANGUAGE PLPGSQL;

+ python call_stored_procedure.py
# BINARIOS
+ python write_blob.py
# BORRADO
python delete.py