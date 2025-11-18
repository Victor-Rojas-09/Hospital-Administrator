# Sistema de Administración Hospitalaria

Este es un proyecto de aplicación de escritorio para la administración simple de hospitales y doctores, desarrollado en Python con PyQt6. El proyecto sigue una arquitectura estricta de 3 capas (Modelo, Controlador, Vista) y aplica buenas prácticas de POO y SOLID.

## Estructura del Proyecto

El proyecto está organizado en una arquitectura de 3 capas, facilitando el mantenimiento y la escalabilidad.

---
* ** `model`:**
    * Contiene las clases de negocio puras: `Hospital` y `Doctor`.
    * Estas clases no saben nada del controlador ni de la interfaz.
    * Utiliza **propiedades (`@property`)** para implementar Getters y Setters, encapsulando los atributos (ej: `_nombre`) y permitiendo un acceso limpio (ej: `doctor.nombre`).

* ** `controller` :**
    * Es el "cerebro" de la aplicación. Contiene toda la **lógica de negocio**.
    * Valida los datos (ej: que el DNI no esté vacío o duplicado).
    * Es el único que tiene permitido **manipular el modelo**. La vista *nunca* toca el modelo directamente.
    * El `HospitalController` no sabe que existe una interfaz gráfica; solo recibe órdenes y devuelve resultados.

* ** `ui` :**
    * Es la capa de presentación. Su única responsabilidad es **mostrar datos** y **capturar la entrada** del usuario.
    * El archivo `ui/main_window.py` contiene las clases `MainWindow` y `OutputWindow`.
    * Estas clases usan la función `loadUi()` de PyQt6 para **cargar dinámicamente** los archivos `.ui` de la carpeta `ui_form_QT`.
    * La Vista **no contiene lógica de negocio**. Cuando un usuario presiona un botón (ej: "Agregar Doctor"), la vista simplemente recolecta el texto de los `QLineEdit` y se lo pasa al controlador.

### Inyección de Dependencias

El flujo de la aplicación sigue el principio de **Inversión de Dependencias**:

1.  **`__main__.py`** se ejecuta primero.
2.  Crea una instancia del `HospitalController`.
3.  Crea una instancia de la `MainWindow`.
4.  **Inyecta** el `controller` en la `MainWindow` a través de su constructor (`__init__`).
