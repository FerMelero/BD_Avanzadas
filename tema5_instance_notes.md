# Tema 5 — notas de instancia (postgresql.conf) para discutir (nivel producción)

Esto NO es un “truco”. Es tuning de la instancia y cambia el foco del laboratorio.
El objetivo aquí es que el estudiante entienda *qué cosas existen* y *qué efectos producen*.

## shared_buffers
- Cache interna de PostgreSQL.
- Si es baja, verás más `Buffers: ... read=...` (I/O real).
- No es “cuanto más mejor”: compite con el SO.

## effective_cache_size
- No reserva memoria.
- Es una pista al optimizador: “cuánta cache total (SO+PG) crees que hay”.
- Si está demasiado bajo, el optimizador puede preferir planes que evitan índices.

## checkpoint_timeout y max_wal_size
- Controlan cada cuánto se fuerzan checkpoints.
- Checkpoints frecuentes ⇒ picos de escritura (I/O) ⇒ carga masiva más lenta.
- En ingestiones grandes, una configuración mala “mata” el throughput.

## work_mem
- Memoria por operación (hash join, sort) y por sesión.
- Subirlo sin pensar puede agotar RAM en concurrencia.

## maintenance_work_mem
- Afecta a CREATE INDEX / VACUUM.
- Útil en fases de carga, dentro de límites seguros.

Regla: si se toca un parámetro, se justifica con evidencia (planes, buffers, stats, comportamiento del sistema).
