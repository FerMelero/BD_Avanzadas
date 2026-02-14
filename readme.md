# README – Estructura de la Base de Datos

## Tablas

### 1. Profesores
| Columna          | Tipo de dato    | Restricciones                 |
|-----------------|----------------|-------------------------------|
| id_profesor      | SERIAL         | PRIMARY KEY                   |
| nombre           | VARCHAR(100)   | NOT NULL                      |
| apellido         | VARCHAR(100)   | NOT NULL                      |
| fecha_nacimiento | DATE           | NOT NULL                      |
| dni              | VARCHAR(20)    | NOT NULL, UNIQUE              |

**Descripción:**  
Cada profesor tiene un identificador único (`id_profesor`) y datos personales.  

---

### 2. Alumnos
| Columna          | Tipo de dato    | Restricciones                 |
|-----------------|----------------|-------------------------------|
| id_alumno        | SERIAL         | PRIMARY KEY                   |
| nombre           | VARCHAR(100)   | NOT NULL                      |
| apellido         | VARCHAR(100)   | NOT NULL                      |
| fecha_nacimiento | DATE           | NOT NULL                      |
| dni              | VARCHAR(20)    | NOT NULL, UNIQUE              |

**Descripción:**  
Cada alumno tiene un identificador único (`id_alumno`) y datos personales.  

---

### 3. Cursos
| Columna      | Tipo de dato    | Restricciones                                         |
|-------------|----------------|-------------------------------------------------------|
| id_curso     | SERIAL         | PRIMARY KEY                                         |
| nombre_curso | VARCHAR(100)   | NOT NULL                                            |
| id_profesor  | INTEGER        | NOT NULL, FOREIGN KEY → profesores(id_profesor)    |

**Relaciones:**  
- Cada curso tiene **1 profesor** asignado (`1:N` con profesores).  
- Al borrar un profesor, los cursos asociados se eliminan (`ON DELETE CASCADE`).  

---

### 4. Matrículas
| Columna     | Tipo de dato    | Restricciones                                      |
|------------|----------------|---------------------------------------------------|
| id_alumno  | INTEGER        | NOT NULL, FOREIGN KEY → alumnos(id_alumno)      |
| id_curso   | INTEGER        | NOT NULL, FOREIGN KEY → cursos(id_curso)        |
|            |                | PRIMARY KEY (id_alumno, id_curso)              |

**Relaciones:**  
- Representa la relación **N:M** entre alumnos y cursos.  
- Cada alumno puede estar en varios cursos y cada curso puede tener varios alumnos.  
- Al borrar un alumno o curso, se eliminan sus matrículas (`ON DELETE CASCADE`).  

---

### Diagrama de relaciones (ERD)

