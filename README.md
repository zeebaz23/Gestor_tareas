# Gestor de tareas
# Descripción del proyecto

El objetivo de este proyecto es desarrollar una aplicación para la gestión de tareas personales y
profesionales. Las funcionalidades que la aplicación debe tener son:

1. Crear una tarea: La aplicación debe permitir a los usuarios crear una tarea en el
sistema

3. Editar una tarea: La aplicación debe permitir a los usuarios editar una tarea existente
en el sistema

5. Eliminar una tarea: La aplicación debe permitir a los usuarios eliminar una tarea
existente en el sistema

7. Iniciar sesión: La aplicación debe permitir a los usuarios iniciar sesión en el sistema con
un usuario ya existente

9. Crear cuenta: Los usuarios deben poder darse de alta en el sistema

10. Cambiar contraseña: El sistema debe permitir a los usuarios cambiar sus contraseñas
cuando ellos lo deseen.

Una tarea debe estar compuesta por los siguientes datos:
1. Texto de la tarea
2. Usuario que creó la tarea
3. Fecha de creación de la tarea
4. Categoría de la tarea
5. Estado de la tarea (Completada, por hacer, en progreso, etc.)
Nota: Cada usuario al crear su cuenta e iniciar sesión debe poder ver sus tareas y solo sus tareas,
no las tareas creadas por los otros usuarios.

# Casos de prueba extremos
- Crear una tarea con texto extremadamente largo

  Descripción: El usuario intenta crear una tarea con un texto muy largo (por ejemplo, 1000 caracteres).

  Pasos:
  Iniciar sesión con un usuario válido.
  Crear una tarea con un texto de 1000 caracteres, seleccionar una categoría y un estado.
  Hacer clic en "Guardar".

  #### Resultado esperado: La tarea se guarda correctamente si el sistema está preparado para manejar textos largos, o se muestra un mensaje de error si el sistema tiene un límite de longitud.
- Eliminar una tarea no existente

  Descripción: El usuario intenta eliminar una tarea que ya ha sido eliminada o no existe.

  Pasos:
  - Iniciar sesión con un usuario válido.
  - Intentar eliminar una tarea que no existe o ya ha sido eliminada.
  #### Resultado esperado: El sistema muestra un mensaje de error indicando que la tarea no se encuentra en la lista.
