# Sprint 3: evidencias reales de Docker y Kafka

Capturadas el **26 de noviembre de 2026**, zona **America/Lima**, para los
apartados **5.3.3.2, 5.3.3.4 y 5.3.3.6** del [capítulo V](../../../capitulos/05-implementacion.md).
Las mismas nueve capturas están insertadas en el
[Word de entrega](../../../entrega/FinanZen-Reporte-Actualizado.docx).
El [registro de integridad del Word](validacion-word.json) conserva los hashes
de sus 43 imágenes anteriores y verifica la incorporación de nueve capturas.

## Capturas y registros originales

| N.º | Evidencia | Captura de CMD | Búfer de consola | Metadatos de captura |
| --- | --- | --- | --- | --- |
| 01 | Repositorio, commits y archivos de configuración | [PNG](01-desarrollo-commits.png) | [TXT](01-desarrollo-commits.txt) | [JSON](01-desarrollo-commits.json) |
| 02 | Dockerfile real del backend | [PNG](02-dockerfile.png) | [TXT](02-dockerfile.txt) | [JSON](02-dockerfile.json) |
| 03 | Validación de Compose, servicios, volúmenes e imágenes | [PNG](03-compose-configuracion.png) | [TXT](03-compose-configuracion.txt) | [JSON](03-compose-configuracion.json) |
| 04 | Versiones Docker/Compose, seis servicios healthy y dos inicializadores Exited (0) | [PNG](04-contenedores-activos.png) | [TXT](04-contenedores-activos.txt) | [JSON](04-contenedores-activos.json) |
| 05 | Verificador integrado: siete comprobaciones aprobadas | [PNG](05-ejecucion-integrada.png) | [TXT](05-ejecucion-integrada.txt) | [JSON](05-ejecucion-integrada.json) |
| 06 | Cuatro health checks HTTP reales | [PNG](06-health-checks.png) | [TXT](06-health-checks.txt) | [JSON](06-health-checks.json) |
| 07 | Logs originales de los cuatro servicios | [PNG](07-logs-servicios.png) | [TXT](07-logs-servicios.txt) | [JSON](07-logs-servicios.json) |
| 08 | Topics y DLQs existentes en Kafka | [PNG](08-kafka-topics-consumidor.png) | [TXT](08-kafka-topics-consumidor.txt) | [JSON](08-kafka-topics-consumidor.json) |
| 09 | Compose up con espera de health checks y servicios activos | [PNG](09-compose-despliegue.png) | [TXT](09-compose-despliegue.txt) | [JSON](09-compose-despliegue.json) |

## Procedencia y alcance

Se ejecutaron comandos reales mediante **cmd.exe** en una ventana local de
Windows Terminal. El prompt `FinanZen>` pertenece a CMD; `cd` muestra el
directorio de trabajo. La terminal no es una página web. El
[script de captura](../../../scripts/capturar_terminal_cmd.py) abre una consola
nativa, espera la terminación de los comandos y captura directamente su ventana
visible con `PIL.ImageGrab`. No dibuja resultados ni modifica las imágenes.

Cada JSON conserva los comandos, sus códigos de salida, fecha con zona horaria,
clase y título de ventana, dimensiones y SHA-256 del PNG. Cada TXT conserva el
búfer de consola, que puede incluir más líneas que el área visible. Las nueve
capturas tienen resolución 1500 × 940 y todos los comandos finalizaron con 0.
Los lotes y marcadores temporales de `_capture/` se excluyen del repositorio.

La ejecución integrada corresponde al modo normal de `scripts/verify_docker.py`:
**7 comprobaciones**, sin `--faults`. El
[JSON original de ejecución](ejecucion-integrada.json) conserva el usuario
sintético `docker-44ecf9af`, los resultados y las posiciones Kafka. La prueba
incluye reentrega idempotente, lectura IoT sin movimiento financiero y cinco
intentos de un mensaje inválido antes de su DLQ. Por ese último escenario aparece
`Kafka message quarantined` en los logs.

Los [health checks completos](health-checks.json) se recibieron por HTTP con el
[script de consulta](../../../scripts/verificar_health_docker.py). La captura 09
verifica la puesta en marcha sobre el stack existente; no documenta una
construcción desde cero ni un despliegue cloud. Los seis servicios permanecieron
activos; las tareas de inicialización terminaron con código 0.

## Código de la ejecución

| Repositorio | Revisión main capturada | Commit de implementación |
| --- | --- | --- |
| back | [f0846ce](https://github.com/1ASI0657-2620-9199/back/commit/f0846ceb886650b425d22ad1c4f940db5915e5f3) | [f92595e](https://github.com/1ASI0657-2620-9199/back/commit/f92595e) |
| front | [b0998d9](https://github.com/1ASI0657-2620-9199/front/commit/b0998d931bb5d29771de3a849f8b9118c2a0a6bc) | [d9af8bd](https://github.com/1ASI0657-2620-9199/front/commit/d9af8bd) |

El archivo real de Docker Compose es **compose.yaml**. Se conservan copias
exactas del [Dockerfile del backend](fuentes-configuracion/backend.Dockerfile),
[compose.yaml](fuentes-configuracion/compose.yaml),
[Dockerfile del frontend](fuentes-configuracion/frontend.Dockerfile) y
[nginx.conf](fuentes-configuracion/nginx.conf). El
[registro de configuración](configuracion-versionada.json) relaciona cada copia
con el repositorio, revisión y hash de contenido.

## Reproducción

Desde `FinanZen/back`, con el checkout hermano `FinanZen/front`, Docker Desktop
activo y las dependencias de `requirements-kafka.txt` instaladas en `.venv`:

```cmd
docker compose config --quiet
docker compose up -d --build --wait --wait-timeout 240
docker compose ps --all
.\.venv\Scripts\python.exe scripts\verify_docker.py
python ..\report\scripts\verificar_health_docker.py
docker compose logs --no-color --tail 6 financial-records budget-service notification-service device-service
```

Para repetir las capturas desde `FinanZen/report`, en Windows con Python,
Pillow, pywin32 y la base de zonas horarias tzdata disponibles:

```cmd
python scripts\capturar_terminal_cmd.py
```

Ese comando ejecuta nuevamente los escenarios y sobrescribe sus capturas; el
verificador crea otro usuario sintético. La copia `ejecucion-integrada.json` y
los snapshots de configuración publicados aquí corresponden a la sesión
documentada. Al preparar otra entrega deben copiarse otra vez desde la ejecución
y revisiones que se quieran documentar.

La [revisión de ramas](revision-ramas.json) registra las referencias publicadas
consultadas en GitHub. La cuenta Darkdren corresponde a Rodrigo Oblitas; los
archivos `.mailmap` de back, front y report unifican la atribución de sus commits.
