# Análisis de redes wifi


En esta etapa tendremos que interacturar con los diferentes componentes de la red que desamos atacar (tantos elementos software como hardware) de forma que encontromos algún protocolo inseguro que podamos explotar con posterioridad.

Dentro de la tecnología wifi encontramos diferentes elementos en los cuales podemos basarnos para detectar vulnerabilidades. Tenemos que tener en cuenta el tipo de cifrado que esta utilizando la red, de forma que si usa WEP sería muy fácil de romper mientras que con WPA la complejidad aumenta.

## Terminologia
Durante las siguientes fases estaremos haciendo referencia a algunas palabras clave relacionadas con las redes wifi, a modo de recopilación dejaré aquí las pricipales:

  * SSID / ESSID : Nombre de la red wifi
  * BSSID : Dirección física (MAC) del router / AP
  * Channel: Canal en el que se encunetra la red wifi que esta emitiendo
  * PWR: Power Range, intensidad con la que nos llega la señal. Lo ideal sería tener una por inferior a -50 para relizar auditorias.
  * ENC y CIPHER: Hace refenrencia al cifrado de la red así como la encriptación

## Canales dentro de las redes wifi

Las redes wifi utilizan ondas de radio que nos permiten comunicarnos a través de una red. Las señales wifi pueden usar un determinado número de canales (13), que les permiten existir diferentes redes sin que exista ruido (interferencias entre ellas) de forma que un canal en el cual no esten confguradas muchas redes wifi tendrá menos interferencias.

Cuando estamos escaneando en busca de redes wifi, será necesario conocer el canal en la que esta emitiendo nuestro objetivo de forma que podamos capturar con posteioridad información relevante.

## Tipos de cifrado en redes wifi

Los principales cifrados que nos encontramos en las redes wireless son:

* WEP (Wired Equivalent Privacy)
* WPA (Wi-Fi Protected Access)
* WPA-2 (Wi-Fi Protected Access II)

Estos procotolos, aunque encargados de cifrar la contraseña evitando que cualquier persona las lea con facilidad, no impiden que puedan ser capturados. Por lo cual, si obtenemos un paquete con la contraseña (aunque este cifrada) si dicha contraseña no es muy compleja será de menos trabajo computacional encontrarla.

La complejidad de la contraseña wifi es importante, sin embargo, no tenemos que olvidar la importancia de aplicar el protocolo adecuado de cifrado. El cifrado WEP es el más antiguo, por lo tanto es másvulnerable al existir más ataques.Estos protocolos han ido evolucionando con el tiempo, de forma que se pudieran solventar las diferentes vulnerabilidades que se iban descubriendo, sin embargo, las vulnerabilidades en estos protocoles siguen apareciendo, una de las más recientes es [Krack](https://papers.mathyvanhoef.com/ccs2017.pdf).

Recientemente se esta comenzando con la implantación de un nuevo protocolo de cifrado WPA3, sin embargo, desde que este protocolo se comienz ha implementar hasta que se convierta en el estándar pasará un considerable periodo de tiempo ( así como paso con la implementación de WPA )

### Wifi Protected Setup (WPS)

Es un protocolo nacido para la facilidad de interconexión entre los diferentes dispositivos, evitando situaciones como compartir contraseñas complejas entre los diferentes dispositivos. WPS, permite acceder a la red mediante un pin de 8 dígitos. Este protocolo, es muy útil en cuanto a funcionalidad, sin embargo, tenemos que tener en cuenta algunos riesgos:

* Un número de 8 dígitos puede llegar a ser crackeado
* Podemos generar el PIN de un router mediante rainbow tables
* Si una serie de routers comparten el mismo pin y este se conoce, todos quedarán expuestos.

Este protocolo generalmente es uno de los más atacados para comprometer las redes wifi, debido a la _"facilidad"_(en comparación con el cracking de contraseñas)de obtener el pin del router.
