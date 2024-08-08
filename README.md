
# Proyecto No. 3: Árboles de Decisión - METSURO

![Metsuro Logo](https://imgur.com/uXfCilV.png)

## Descripción Breve
El objetivo del programa es crear un modelo que prediga el valor de una variable objetivo basado en varias variables de entrada. 

## Instalación
Para instalar y configurar el programa, se deben seguir estos pasos:

1. **Clonar el Repositorio**:
    Primero, se clona el repositorio a su máquina local utilizando el siguiente comando:
    ```
    git clone https://github.com/migurd/decision-tree
    cd decision-tree
    ```

2. **Crear y Activar el Entorno Virtual**:

    **En Windows:**
    ```
    python -m venv venv
    venv\Scripts\activate
    ```

    **En Linux/Mac:**
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Instalar las Dependencias**:
    Con el entorno virtual activado, se instala las dependencias necesarias ejecutando:
    ```
    pip install -r requirements.txt
    ```

## Funcionalidades del Programa

1. **Carga de Datos Manual**
    - Se define el número de atributos a considerar (mínimo 3 y máximo 5) incluyendo la Clase (+/-).
    - Se permite que los valores de los atributos sean ingresados de forma aleatoria, manual o importados.

2. **Identificación de Atributos**
    - Se determina si cada atributo es nominal o numérico.
    - Para atributos nominales, se permite la inclusión de 2 o 3 valores posibles: Bajo (1), Normal (2) y Alto (3).
    - Para atributos numéricos, se incluye dos valores numéricos X1 y X2 y clasificar cada instancia como: <X1, X1-X2 o >X2.

3. **Atributo Clase**
    - Se usa el valor 1 para la clase positiva y el valor 0 para la clase negativa.

4. **Salida del Programa**
    - Se muestra la tabla final con los valores de cada instancia incluyendo la clase.
    - Se calcula y muestra la entropía general.
    - Se calcula y muestra la ganancia de información para cada atributo.
    - Se determina y muestra cuál deberá ser el nodo raíz.

## Cómo probar
    - Importar archivo en la ruta src/Tenis.xlsx