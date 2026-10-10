workspace "FinanZen Deployment" "Financial Records Service desplegado con PostgreSQL persistente" {
    model {
        user = person "Usuario de demostración" "Usa Swagger o un cliente Postman mediante HTTPS"
        finanzen = softwareSystem "FinanZen" "Incremento de registros financieros" {
            api = container "Financial Records API" "Registro idempotente, consulta y resumen mensual" "Python 3.11 / FastAPI / Uvicorn"
            database = container "Financial Records Database" "Tabla transactions y claves idempotentes persistentes" "PostgreSQL 17" {
                tags "Database"
            }
        }
        user -> api "Registra y consulta movimientos" "HTTPS / JSON"
        api -> database "Lee y escribe movimientos" "PostgreSQL pooled / TLS verificado"
        production = deploymentEnvironment "Production" {
            deploymentNode "Equipo del usuario" "Cliente de demostración" "Navegador / Postman" {
                client = infrastructureNode "Cliente HTTPS" "Swagger UI o Postman" "HTTPS"
            }
            deploymentNode "Render" "Web Service Free; Virginia" "Render Free" {
                deploymentNode "finanzen-financial-records" "srv-db4vl25ckfvc738e4hp0; /health; 0.0.0.0:$PORT" "Python runtime" {
                    apiRuntime = containerInstance api
                }
            }
            deploymentNode "Neon" "Organización Free; aws-us-east-1" "Neon Free" {
                deploymentNode "dawn-bird-07958545" "Conexión privada DATABASE_URL; compute independiente" "PostgreSQL 17" {
                    containerInstance database
                }
            }
        }
        client -> apiRuntime "Registra y consulta movimientos" "HTTPS / JSON"
    }
    views {
        deployment finanzen production "FinanZenDeployment" "Infraestructura implementada, verificada el 10 de octubre de 2026" {
            include *
            autoLayout lr
        }
        styles {
            element "Element" {
                color #ffffff
                background #1168bd
            }
            element "Database" {
                shape Cylinder
            }
            element "Deployment Node" {
                color #223344
                background #f0f5fa
            }
        }
    }
}
