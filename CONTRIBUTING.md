# Contribuyendo al TECcrBOT
Gracias por apoyar esta herramienta de aporte a la comunidad estudiantil.

Estas son algunas pautas y recomendaciones para aportar al tanto al código del proyecto como la base de datos. En su mayoría esta es una guía mas no reglas. Use su mejor criterio y siéntase libre proponer cambios a esta guía en un pull request.

# Tabla de contenidos

- [Contribuyendo al TECcrBOT](#contribuyendo-al-teccrbot)
- [Tabla de contenidos](#tabla-de-contenidos)
- [Solo tengo unas preguntas, no quiero leer toda esta guía](#solo-tengo-unas-preguntas-no-quiero-leer-toda-esta-gua)
- [Por donde empezar](#por-donde-empezar)
  - [Contribuir al código del bot](#contribuir-al-cdigo-del-bot)
  - [Contribuir a la base de datos](#contribuir-a-la-base-de-datos)

# Solo tengo unas preguntas, no quiero leer toda esta guía
Si tiene preguntas no abra un issue en el repositorio, puede usar los siguientes medios para resolver sus dudas.

- Puede enviar un mensaje a Alejandro Díaz por telegram en [@adiazp](https://t.me/adiazp).

# Por donde empezar
Este proyecto se compone de dos grandes ramas, el código fuente del bot y la base de datos que guarda toda la información que puede proveer.

## Contribuir al código del bot
Las tecnologías principales actualmente utilizadas son: [Python](https://www.python.org/), [Django](https://www.djangoproject.com/) y [telegram-bot-api](https://github.com/python-telegram-bot/python-telegram-bot). Conocer estas herramientas le permitirá entender mejor la estructura del proyecto y generar mejores aportes.

Para ejecutar el proyecto, refiérase a las instrucciones dejadas en el [README.md](README.md) principal.

### Parar reportar un bug
Si ha encontrado algún bug puede reportarlo creando una issue usando la plantilla designada y la etiqueta "bug". De esta manera será más fácil para cualquier desarrollador encontrar los reportes y resolverlos.

### Para proponer cambios
Para proponer cambios puede crear una issue indicando los detalles de su propuesta y el beneficio que traería integrar tales cambios, luego puede crear un pull request relacionado a dicha issue con el fin de que sus cambios sean integrados.

## Contribuir a la base de datos
La base de datos se compone de una serie de archivos json que al ser desplegados en producción se genera una instancia utilizando algún RDBMS (PostgreSQL, SQLite). El bot proporciona variados tipos de información tales como contactos de personas, ubicaciones de interés, información de tutorías, entre otros. Para conocer los detalles de cada tipo y cómo ayudar refiérase a []() en la wiki.

