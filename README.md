# Honeypot-educativo-sena

Este proyecto simula un honeypot básico en Python para detectar intentos de conexión no autorizados en un entorno académico. Está diseñado como herramienta educativa para fomentar el aprendizaje en ciberseguridad, especialmente en el contexto de redes simuladas o laboratorios de formación.

## Objetivos

- Comprender el funcionamiento de un honeypot pasivo.
- Registrar y analizar intentos de conexión en tiempo real.
- Promover buenas prácticas en seguridad digital dentro del SENA.

## Tecnologías utilizadas

- Python 3
- Socket
- Logging con rotación (`RotatingFileHandler`)
- JSON para estructurar los logs
- Multithreading (`threading`)
- Manejo de señales (`signal`)
- Apagado automático por inactividad(`opcional`)

## Instalación y ejecución

1. Clona el repositorio:
   ```bash
   # git clone https://github.com/MIGUEL-ANGEL000/honeypot-educativo-sena.git
   cd honeypot-educativo-sena
   python honeypot.py
para detener la ejecucion presiona CTRL+C
## Archivos generados
- cuando se detecta un intento de acceso  se genera un registro en honeypot_logs
- cuando el archivo honeypot_logs supera los 5kb des espacio se genera otro archivo honeypot_logs2,3,4...
- cualquier error de documenta en el archivo log
## Resultados esperados
- Registro de IPs, puertos y marcas de tiempo.
- Análisis básico de comportamiento sospechoso.
- Evidencia útil para formación en ciberseguridad.
- Código modular y reutilizable para otros proyectos educativos

## como esto es un prototipo agradeceria que me dieran sugerencias de como mejorarlo y si me mandan contenido educativo sobre el tema estaria increible  thanks B)


   
