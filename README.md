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

## Registro de versiones

| Versión documental | Fecha | Base | Cambios |
| --- | --- | --- | --- |
| Hito 1 conservado | Fecha no indicada | README previo del repositorio | Introducción, competidores y diseño de entrevistas |
| Actualización del informe | 2026-10-10 | PDF proporcionado y código del MVP | Datos de portada corregidos; capítulos II–V ampliados; fuentes y figuras conservadas y evidencia reproducible |
| Repositorios independientes | 2026-10-10 | Organización 1ASI0657-2620-9199 | Cinco repositorios: back, report, landing, front y mobile; enlaces, ejecución y validaciones adaptados |
| Evidencias del Sprint 1 | 2026-10-10 | Backend/API existentes y statement 202620 | Capítulo V ampliado: Repository, configuración, diagrama local, commits, endpoints, respuestas reales, log de pruebas y guía de capturas/video |
| Persistencia y capturas | 2026-10-10 | Backend con SQLite/PostgreSQL y ejecución HTTP local | Render Free + Neon preparado, 8 tests, 11 comprobaciones Newman, 13 capturas y grabación real; publicación cloud pendiente de acceso a las herramientas |
| Deployment cloud | 2026-10-10 | Render Free y Neon Free reales | API Live, URL HTTPS, 13 capturas públicas adicionales, grabación, 8 peticiones/11 aserciones Newman y persistencia tras reiniciar Render |

**API pública:** [Swagger](https://finanzen-financial-records.onrender.com/docs)
· [Health](https://finanzen-financial-records.onrender.com/health)
· [Evidencias del deployment](evidencias/deployment/publico/README.md).

El PDF no registra fechas ni autores en su tabla de versiones. Esta tabla
documenta los artefactos disponibles, sin atribuir nuevas entrevistas ni
trabajo de desarrollo a integrantes específicos.

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
   incremento implementado, configuración, pruebas, evidencias y pendientes.
6. [Evidencia reproducible de esta entrega](evidencias/validacion.md).
7. [PDF original](fuentes/TF_1ASI0657_202610_NRC_7.pdf),
   [transcripción completa](fuentes/transcripcion_pdf.md),
   [enlaces del PDF](fuentes/enlaces_pdf.md) y [figuras](assets/README.md).
8. [README del hito anterior](historico/README_hito1.md).
9. [Evidencias del Sprint 1 y archivos por agregar](evidencias/sprint-1/README.md),
   con colección de Postman y resultados reales de la API.
10. [Deployment y capturas incorporadas](evidencias/deployment/README.md):
    logs, Swagger, Newman, persistencia y grabación; estado del despliegue público.

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

| Componente | Evidencia actual | Pendientes |
| --- | --- | --- |
| [Back](https://github.com/1ASI0657-2620-9199/back/blob/main/README.md) | FastAPI, SQLite/PostgreSQL, registros idempotentes, resumen, 8 pruebas y deployment Render Free/Neon Free verificado | Identidad real, presupuesto, eventos, IoT, análisis, educación y auditoría |
| [Front](https://github.com/1ASI0657-2620-9199/front/blob/main/README.md) | Panel web conectado a la API | Autenticación y pantallas de las capacidades pendientes |
| [Landing](https://github.com/1ASI0657-2620-9199/landing/blob/main/README.md) | Repositorio preparado, sin código | Diseño, implementación y contenido de US13/US14 |
| [Mobile](https://github.com/1ASI0657-2620-9199/mobile/blob/main/README.md) | Repositorio preparado, sin código | Implementación del cliente móvil |

Las capacidades del MVP no completan todos los criterios de US01 ni los de
US10–US12. El resumen mensual aporta una base a PF-02; presupuestos, alertas
y reportes semanales siguen pendientes. El aislamiento por `X-User-Id` no
constituye autenticación y no demuestra el cumplimiento íntegro de QA-01.

## Apartados pendientes en el PDF

Student Outcome, perfiles individuales del equipo, configuración de despliegue,
evidencia de despliegue en nube, colaboración y Kanban tienen desarrollo ausente
o insuficiente en la fuente. Esta actualización completa configuración y
evidencias de deployment Render/Neon con una URL real y persistencia remota.
Student Outcome, perfiles, colaboración, Kanban y resultados de carga requieren
sus actividades reales. El capítulo V detalla esos límites.
