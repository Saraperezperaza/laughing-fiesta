[ProSalud]
[//]: ProSalud es una aplicación médica innovadora desarrollada para optimizar la gestión de la información sanitaria. Su objetivo principal es facilitar la administración eficiente de los datos relacionados con pacientes y profesionales de la salud, proporcionando un sistema ágil y seguro para mejorar la calidad de la atención médica.

Autores
(Coordinador) María Mestre Sánchez (https://github.com/mms254)
Carla Carreras Villarejo (https://github.com/carlacarreras)
Alicia Frías Gonzalez (https://github.com/amfg15)
Ricardo López Moya (https://github.com/rrricardoua23)
Sara Pérez Peraza (https://github.com/Saraperezperaza)
Profesor
[//]: Miguel Ángel Teruel Miguel A. Teruel

Requisitos
[//]:Informe médico final de cada paciente en pdf y calendario de citas de cada paciente también. (Ricardo)

 Permitirá la gestión de usuarios (pacientes dados de alta, baja, graves, menores, ancianos...) y roles de sistema (pacientes, médicos, enfermeros, limpieza...) . (Carla) 
 
 Realización de una base de datos donde estas registrados los trabajadores, pacientes, centros... (Sara) 
 
 Gestión para pedir citas (telefónicas, online, urgencias...) (María)  
 
 Sistema de recomendación de medicamentos según los síntomas del paciente, modo farmacia online (Alicia) 
 
 Uso de API  médica (para los medicamentos), identificar de que medicamente se trata (Alicia) 
 
 Asociar un paciente con su medico de cabecera  de manera aleatoria y luego recargar la base de datos (María)
 
 Según edad y tipo de paciente, alergia o demás ítems  calendario de vacunación. (Carla) 
 
 Gestión de habitaciones para los pacientes según si están libres, ocupadas, si son de la UCI, box... (Ricardo) 
 
 Creación de SIP de cada paciente cuando se da de alta con la  información  correspondiente (Sara)  
Instrucciones de instalación y ejecución
[//]: Para poder ejecutar el código de Prosalud, necesitaréis descargar las siguientes librerías: bcrypt (para el cifrado de contraseñas en los usuarios), reportlab (para los informes en pdf), request (para la API médica externa) y flask (para las APIS internas). Luego, una vez intaladas estas librerías se puede proceder a ejecutar el código, que nos mostrará en la terminal dos menús: de paciente y de médico, al seleccionar alguna opción se ejecutará el código de alguno de los requisitos anteriores, permitiendo al usuario múltiples opciones

Resumen de la API:
Se aplican 5 APIS, la primera es la primera y única API externa, cuyo objetivo es tener información real sobre medicamentos y relacionarlos con los síntomas del paciente. La siguientes son APIS internas, estas son la API de los usuarios que permitirá crear nuevos usuarios, la gestión de habitaciones según si están libres u ocupadas, el informe médico final en pdf y la creación del SIP de los pacientes cuando estos se dan de alta. Es necesario aclarar que para poder seleccionar cualquiera de estas opciones dentro del menú se debe ejecutar anteriormente el fichero llamado apis_Prosalud, donde residen todas las apis. [//]: # (Cuando tengáis la API, añadiréis aquí la descripción de las diferentes llamadas.) [//]: # (Para la evaluación por pares, indicaréis aquí las diferentes opciones de vuestro menú textual, especificando para qué sirve cada una de ellas)
