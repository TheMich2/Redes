# Diagrama de Base de Datos - Sistema de Monitoreo de Red

## Descripción

Este diagrama representa la estructura de la base de datos `redes_tecnologico` para el sistema de monitoreo del Instituto Tecnológico de Oaxaca.

## Relaciones

- **core → switches**: 1:N — Un core tiene varios switches conectados.
- **switches → telefonos**: 1:N — Un switch conecta varios teléfonos IP.
- **edificios → telefonos**: 1:N — Un edificio agrupa varios teléfonos (para el mapa).
- **switches → edificios**: 1:1 opcional — Un edificio puede tener un switch asociado.

## Diagrama ER (Mermaid)

Para visualizar: copia el bloque siguiente en [Mermaid Live Editor](https://mermaid.live) o usa una extensión de Mermaid en VS Code.

```mermaid
erDiagram
    core ||--o{ switches : "tiene"
    switches ||--o{ telefonos : "conecta"
    edificios ||--o{ telefonos : "agrupa"
    switches ||--o| edificios : "asociado a"

    core {
        int id PK
        varchar nombre
        varchar ip_management
        varchar descripcion
        timestamp creado_en
    }

    switches {
        int id PK
        int core_id FK
        varchar nombre
        varchar ip_management
        varchar ubicacion
        decimal lat
        decimal lng
        tinyint ultimo_ping_ok
        timestamp ultimo_ping_at
        timestamp creado_en
    }

    edificios {
        int id PK
        varchar nombre UK
        varchar ubicacion
        decimal lat
        decimal lng
        int switch_id FK
        timestamp creado_en
    }

    telefonos {
        int id PK
        int switch_id FK
        int edificio_id FK
        varchar extension UK
        varchar ip
        varchar mac
        int vlan_id
        varchar ubicacion
        varchar modelo
        decimal lat
        decimal lng
        tinyint activo
        tinyint ultimo_ping_ok
        timestamp ultimo_ping_at
        timestamp creado_en
        timestamp actualizado_en
    }

    usuarios {
        int id PK
        varchar usuario UK
        varchar password_hash
        varchar nombre
        varchar rol
        tinyint activo
        timestamp creado_en
    }
```

## Diagrama de flujo de datos (topología)

```
                    ┌─────────┐
                    │  core   │
                    └────┬────┘
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
      ┌──────────┐ ┌──────────┐ ┌──────────┐
      │ switch 1  │ │ switch 2  │ │ switch N  │
      └────┬─────┘ └────┬─────┘ └────┬─────┘
           │            │            │
     ┌─────┴─────┐ ┌────┴────┐ ┌────┴────┐
     ▼           ▼ ▼         ▼ ▼         ▼
┌─────────┐ ┌─────────┐  ┌─────────┐
│teléfono │ │teléfono │  │teléfono │  ...
└─────────┘ └─────────┘  └─────────┘

     edificios (agrupan teléfonos por ubicación en el mapa)
```
