# Architecture

```text
                COMMAND CENTER UI
                       |
                FastAPI API Layer
                       |
       +---------------+---------------+
       |               |               |
       v               v               v
   Zero Trust      PQC Migration    AI/Asset Health
   Trust state     crypto posture   failure/RUL
       |               |               |
       +---------------+---------------+
                       |
                       v
               Correlation Engine
                       |
                       v
                Resilience Score
                       |
                       v
               Human Decision Layer
```

The digital twin is synthetic. No control path exists from the dashboard to physical equipment.
