# FinanZen — Informe del proyecto

Trabajo final de **1ASI0657 — Fundamentos de Arquitectura de Software**,
Universidad Peruana de Ciencias Aplicadas. Periodo **202620**, NRC **9199**.
Profesor: **Daniel Enrique Mori Yzaguirre**.

**Enlace común:** [repositorios de FinanZen](https://github.com/orgs/1ASI0657-2620-9199/repositories).

Cada componente tiene su propio repositorio e historial Git. Este repositorio contiene exclusivamente el informe y sus fuentes.

## Integrantes

| Integrante | Código |
| --- | --- |
| Oblitas Alcalde Rodrigo | U20221G185 |
| Revilla Quispe Renzo Zamir | U201717085 |
| Aguirre Eneque Joan Elias | U202315649 |

La cuenta GitHub **[Darkdren](https://github.com/Darkdren)** pertenece a
**Rodrigo Oblitas**. Los commits registrados con ese nombre corresponden a
Rodrigo; `.mailmap` unifica su atribución en Git y conserva el historial.

## Registro de versiones

| Versión documental | Fecha | Base | Cambios |
| --- | --- | --- | --- |
| Hito 1 conservado | Fecha no indicada | README previo del repositorio | Introducción, competidores y diseño de entrevistas |
| Actualización del informe | 2026-10-10 | PDF proporcionado y código del MVP | Datos de portada corregidos; capítulos II–V ampliados; fuentes y figuras conservadas y evidencia reproducible |
| Repositorios independientes | 2026-10-10 | Organización 1ASI0657-2620-9199 | Cinco repositorios: back, report, landing, front y mobile; enlaces, ejecución y validaciones adaptados |
| Evidencias del Sprint 1 | 2026-10-10 | Backend/API existentes y statement 202620 | Capítulo V ampliado: Repository, configuración, diagrama local, commits, endpoints, respuestas reales, log de pruebas y guía de capturas/video |
| Persistencia y capturas | 2026-10-10 | Backend con SQLite/PostgreSQL y ejecución HTTP local | Configuración Render Free + Neon, 8 tests, 11 comprobaciones Newman, 13 capturas y grabación de ejecución |
| Deployment cloud | 2026-10-10 | Render Free y Neon Free reales | API Live, URL HTTPS, 13 capturas públicas adicionales, grabación, 8 peticiones/11 aserciones Newman y persistencia tras reiniciar Render |
| Cierre técnico del Sprint 1 | 2026-10-10 | Backend v0.1.1 y biblioteca 0.1.0 | Doce pruebas, seis escenarios Gherkin locales y cinco públicos, GitFlow con tres PR, release con wheel/sdist, C4 Deployment, Trello real y video explicado |
| Docker y Kafka del Sprint 3 | 2026-11-26 | back f0846ce y front b0998d9 | Apartados 5.3.3.2, 5.3.3.4 y 5.3.3.6 en Markdown y Word: nueve capturas reales de CMD, siete comprobaciones integradas, seis servicios saludables, logs y health checks |
| Atribución y revisión del informe | 2026-11-26 | Confirmación del titular y revisión de ramas GitHub | Darkdren identificado como Rodrigo Oblitas; redacción revisada en Markdown y Word; historial develop de back incluido en main |

**API pública:** [Swagger](https://finanzen-financial-records.onrender.com/docs)
· [Health](https://finanzen-financial-records.onrender.com/health)
· [Evidencias del deployment](evidencias/deployment/publico/README.md).
· [Evidencias del cierre del Sprint 1](evidencias/cierre-sprint-1/README.md).

Documento compartido: [Google Docs del equipo](https://docs.google.com/document/d/1Q70r6_MAmjk9BNTKyIEDe3r9cuEV_UPJrb6Ec3v47Tk/edit?tab=t.0).

La actualización histórica del capítulo V en el documento compartido contiene veinte apartados
verificados, tablas y enlaces a diecinueve imágenes de evidencia distintas.
Los capítulos anteriores se conservaron. El
[Word de entrega](entrega/FinanZen-Reporte-Actualizado.docx) integra las figuras.
[Verificación de la actualización histórica](evidencias/cierre-sprint-1/google-doc-update.json).

**Versión del 26 de noviembre:** el [capítulo V](capitulos/05-implementacion.md) y
el [Word de entrega](entrega/FinanZen-Reporte-Actualizado.docx) contienen los
apartados de desarrollo, ejecución y despliegue de Docker/Kafka del Sprint 3.
El [índice de Sprint 3](evidencias/sprint-3/docker/README.md) permite consultar las
nueve capturas de CMD y sus registros originales.

La tabla de versiones relaciona las entregas con sus artefactos y fechas de
verificación. El PDF conserva la tabla de versiones de la fuente original.

## Contenido

1. [Capítulo I: Introducción](capitulos/01-introduccion.md): startup, solución,
   5W2H, Lean UX y segmentos objetivo.
2. [Capítulo II: Requirements Elicitation & Analysis](capitulos/02-elicitacion.md):
   competidores, siete entrevistas, hallazgos, personas, matrices y mapas.
3. [Capítulo III: Requirements Specification](capitulos/03-especificacion.md):
   To-Be, cinco épicas, 14 historias con criterios, Impact Map y backlog.
4. [Capítulo IV: Product Architecture Design](capitulos/04-arquitectura.md):
   principios, vistas, drivers, escenarios de calidad y cinco iteraciones ADD.
5. [Capítulo V: Product Implementation, Validation & Deployment](capitulos/05-implementacion.md):
   incremento implementado, configuración, pruebas y evidencias de ejecución.
6. [Evidencia reproducible de esta entrega](evidencias/validacion.md).
7. [PDF original](fuentes/TF_1ASI0657_202610_NRC_7.pdf),
   [transcripción completa](fuentes/transcripcion_pdf.md),
   [enlaces del PDF](fuentes/enlaces_pdf.md) y [figuras](assets/README.md).
8. [README del hito anterior](historico/README_hito1.md).
9. [Evidencias del Sprint 1](evidencias/sprint-1/README.md),
   con colección de Postman y resultados reales de la API.
10. [Deployment y capturas incorporadas](evidencias/deployment/README.md):
    logs, Swagger, Newman, persistencia y grabación; estado del despliegue público.
11. [Cierre del Sprint 1](evidencias/cierre-sprint-1/README.md): librería,
    Gherkin, C4, GitFlow, tablero, video narrado y release desplegada.
12. [Reporte Word con evidencias integradas](entrega/FinanZen-Reporte-Actualizado.docx).
13. [Docker y Kafka del Sprint 3](evidencias/sprint-3/docker/README.md): desarrollo,
    ejecución integrada y despliegue local con capturas reales de CMD.
14. [Manual para la demostración](entrega/Manual-Demostracion-FinanZen.pdf),
    [Word editable](entrega/Manual-Demostracion-FinanZen.docx) y
    [guion breve](entrega/Guion-Demostracion-FinanZen.txt): recorrido de la app,
    cuentas de ensayo y explicación para la presentación.

## Criterio de actualización

La fuente es `TF_1ASI0657_202610_NRC_7.pdf`, de 109 páginas físicas. Su índice
contiene referencias a páginas mayores que la extensión real del archivo;
las referencias de esta adaptación utilizan páginas físicas. El PDF se conserva
sin modificar, incluidos sus recursos visuales y evidencias históricas.

SHA-256 del PDF original:

```text
b81f72f9f9c03d0c70d0dcd8934043ee67e3286bf2df98885a912e1040bbdc58
```

El informe adapta y organiza el contenido, conserva las historias y separa
lo propuesto de lo implementado.

## Estado de los componentes

| Componente | Implementación publicada | Ejecución y documentación |
| --- | --- | --- |
| [Back](https://github.com/1ASI0657-2620-9199/back/blob/main/README.md) | Financial Records, Budget, Notification y Device Integration; Outbox, consumidores idempotentes, Kafka y DLQs | Cuatro APIs FastAPI, Swagger por servicio, suites automatizadas y Docker Compose |
| [Front](https://github.com/1ASI0657-2620-9199/front/blob/main/README.md) | Panel de movimientos, presupuestos, alertas, dispositivos y reportes | Nginx con gateway HTTP hacia las cuatro APIs; puerto local 8080 |
| [Landing](https://github.com/1ASI0657-2620-9199/landing/blob/main/README.md) | Repositorio del componente landing | README del componente |
| [Mobile](https://github.com/1ASI0657-2620-9199/mobile/blob/main/README.md) | Repositorio del componente móvil | README del componente |

El flujo integrado procesa TransactionRecorded, actualiza el presupuesto y
entrega una notificación cuando se alcanza su umbral. Device Integration
normaliza lecturas de consumo y conserva la telemetría en una base independiente.
Los escenarios utilizan X-User-Id como identidad de demostración.

La [revisión de ramas](evidencias/sprint-3/docker/revision-ramas.json) registra
las referencias consultadas en GitHub. El historial de `develop` del backend
forma parte de `main`.
