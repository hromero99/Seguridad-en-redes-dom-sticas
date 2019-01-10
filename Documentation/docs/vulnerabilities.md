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

### Funcionamiento del protocolo WPA2

En este escenario se va a simular uno de los casos más comunes, una red con cifrado WPA PSK (Pre Shared Key). Antes de continuar con la obtención de la contraseña, pasaremos a explicar como funciona el cifrado WPA2 y que es el 4-Way-Handsake.

El cifrado WPA se implementó aumentando la seguridad existente en su predecesor WPA, para ello se cambio el tipo de cifrado que se utilizaba, siendo AES (Advanced Encription Standard) el que implenta WPA2. WPA2 queda implementado con el estándar [IEEE 802.11 i](https://es.wikipedia.org/wiki/IEEE_802.11i-2004). Este estándar proveía RsN (Robust Security Network), para lo cual fue necesario la implementación de 2 protocolos:
* Four-Way Handsake
* Group Key Hansake

El estándar proveía de dos protocolos de integridad y confidencialidad de datos: CCMP y TKIP, siendo este último el más robusto puesto que CCMP se implementó para obtener compatibilidad con los routers que soportaban cifrado WEP.

WPA2 realiza una autenticacicón inicial mediante PSK (Pre Shared Key) o siguiendo un cambio EAP mediante el estándar 802.1x (implementación em Linux bajo wpa_supplicant), sin embargo este último método requiere un servidor EAPOL de autenticación, por lo cual en entornos domésticos es menos usual encontrarlo. Esta contraseña compartida permite asegurar que el dispositivo que quiere conectarse esta autenticado en el punto de acceso.

Posterior a este intercambio de claves, se procede a la generación de una clave privada denominada PMK(Pairwise Master Key), la cual es el resultado de pasar la contraseña a la función criptográfica PBKDF2-SHA1. Cuando nos encontramos en una Pre-Shared-Key Network la PMK y PSK coinciden.

#### Four-Way Handsake

El protocolo Four-Way Handsake fue ideado con la intención de que el AP (Access Point) y el cliente puedan probar que conocen las claves PSK/PMK sin necesidad de revelar dicha clave. Para poder realizar esto el AP y el cliente encriptan los mensajes y se los envían al otro (dichos mensajes se pueden desencriptar con la PMK), si se logra desencriptarlos correctamente se demuestra que tienen conocimiento de la PSK.

Four-Way Handsake usa una PTK(Pairwise Transient Key), la cual esta compuesta por una combinanción de :

* PMK
* AP nonce (ANonce) y STA nonce (SNonce)
* AP Mac
* STA Mac

El producto de estos valores introducido en una funcuión pseudoaleatoria tiene como resultado la PTK. El Handsake contiene también la GTK (Group Temporal Key), la cual es usada para desencriptar el tráfico de multicast y broadcast.

![Four-Way Handsake](img/4-way-handshake.png)

1. El AP envía un paquete Anonce (el cual contiene un valor que solo puede ser usado una vez en una función criptográfica) y un Key Replay Counter encargado de llevar la cuenta de los parquetes que se han transmitido.

2. El cliente (STA) responde con SNonce junto con un MIC (Message Integrity code), el cual incluye aunteticación, por lo tanto es un MAIC (Message Authentication Integrity Code) y el Key Replay Counter

3. El AP comprueba si el mensaje 2 es correcto mediante los campos MIC, Key Replay Counter, MIC, Anonce y RSN. Si el mensaje es correcto pasará a generar la GTK con otro MIC.

4. El STA verifica los datos del mensaje 3 y si es válido envía confirmación al AP.

Este protocolo es vulnerable a KRACK, la cual fue parcheda adecuadamente. Sin embargo, se observaba que en 2018 existían dispositivos sin actualizar que podian ser vulnerables.



### Wifi Protected Setup (WPS)

Es un protocolo nacido para la facilidad de interconexión entre los diferentes dispositivos, evitando situaciones como compartir contraseñas complejas entre los diferentes dispositivos. WPS, permite acceder a la red mediante un pin de 8 dígitos. Este protocolo, es muy útil en cuanto a funcionalidad, sin embargo, tenemos que tener en cuenta algunos riesgos:

* Un número de 8 dígitos puede llegar a ser crackeado
* Podemos generar el PIN de un router mediante rainbow tables
* Si una serie de routers comparten el mismo pin y este se conoce, todos quedarán expuestos.

Este protocolo generalmente es uno de los más atacados para comprometer las redes wifi, debido a la _"facilidad"_(en comparación con el cracking de contraseñas)de obtener el pin del router.
