# Análisis de redes wifi


En esta etapa tendremos que interacturar con los diferentes componentes de la red que desamos atacar (tantos elementos software como hardware) de forma que encontramos algún protocolo inseguro que podamos explotar con posterioridad.

Dentro de la tecnología wifi encontramos diferentes elementos en los cuales podemos basarnos para detectar vulnerabilidades. Tenemos que tener en cuenta el tipo de cifrado que está utilizando la red, de forma que si usa WEP sería muy fácil de romper mientras que con WPA la complejidad aumenta.

## Terminología
Durante las siguientes fases estaremos haciendo referencia a algunas palabras clave relacionadas con las redes wifi, a modo de recopilación dejaré aquí las pricipales:

  * SSID / ESSID : Nombre de la red wifi
  * BSSID : Dirección física (MAC) del router / AP
  * Channel: Canal en el que se encunetra la red wifi que esta emitiendo
  * PWR: Power Range, intensidad con la que nos llega la señal. Lo ideal sería tener una por inferior a -50 para realizar auditorias.
  * ENC y CIPHER: Hace referencia al cifrado de la red así como la encriptación

## Canales dentro de las redes wifi

Las redes wifi utilizan ondas de radio que nos permiten comunicarnos a través de una red. Las señales wifi pueden usar un determinado número de canales (13), que les permiten existir diferentes redes sin que existan interferencias, de forma que un canal en el cual no esten confguradas muchas redes wifi tendrá menos interferencias.

Cuando estamos escaneando en busca de redes wifi, será necesario conocer el canal en el que esta emitiendo nuestro objetivo de forma que podamos capturar con posteridad información relevante.

## Tipos de cifrado en redes wifi

Los principales cifrados que nos encontramos en las redes wireless son:

* WEP (Wired Equivalent Privacy)
* WPA (Wi-Fi Protected Access)
* WPA-2 (Wi-Fi Protected Access II)

Estos procotolos, aunque encargados de cifrar la contraseña evitando que cualquier persona las lea con facilidad, no impiden que puedan ser capturados. Por lo cual, si obtenemos un paquete con la contraseña (aunque este cifrada) si dicha contraseña no es muy compleja será de menos trabajo computacional encontrarla.

La complejidad de la contraseña wifi es importante, sin embargo, no tenemos que olvidar la importancia de aplicar el protocolo adecuado de cifrado. El cifrado WEP es el más antiguo, por lo tanto es más vulnerable al existir más ataques.Estos protocolos han ido evolucionando con el tiempo, de forma que se pudieran solventar las diferentes vulnerabilidades que se iban descubriendo, sin embargo, las vulnerabilidades en estos protocolos siguen apareciendo, una de las más recientes es [Krack](https://papers.mathyvanhoef.com/ccs2017.pdf).

Recientemente se esta comenzando con la implantación de un nuevo protocolo de cifrado WPA3, sin embargo, desde que este protocolo se comience ha implementar hasta que se convierta en el estándar pasará un considerable periodo de tiempo ( así como paso con la implementación de WPA )

### Funcionamiento del protocolo WPA2

En este escenario se va a simular uno de los casos más comunes, una red con cifrado WPA PSK (Pre Shared Key). Antes de continuar con la obtención de la contraseña, pasaremos a explicar como funciona el cifrado WPA2 y que es el 4-Way-Handsake.

El cifrado WPA se implementó aumentando la seguridad existente en su predecesor WPA, para ello se cambio el tipo de cifrado que se utilizaba, siendo AES (Advanced Encription Standard) el que implenta WPA2. WPA2 queda implementado con el estándar [IEEE 802.11 i](https://es.wikipedia.org/wiki/IEEE_802.11i-2004). Este estándar proveía RsN (Robust Security Network), para lo cual fue necesario la implementación de 2 protocolos:

* Four-Way Handsake, usado para para la autenticación
* Group Key Hansake, usado para validar el tráfico multicast y de broadcast

El estándar proveía de dos protocolos de integridad y confidencialidad de datos: CCMP y TKIP, siendo este último el más robusto puesto que CCMP se implementó para obtener compatibilidad con los routers que soportaban cifrado WEP.

WPA2 realiza una autenticacicón inicial mediante PSK (Pre Shared Key) o siguiendo un cambio EAP mediante el estándar 802.1x (implementación en Linux bajo [wpa_supplicant](https://w1.fi/wpa_supplicant/)), sin embargo este último método requiere un servidor EAPOL de autenticación, por lo cual en entornos domésticos es menos usual encontrarlo. Esta contraseña compartida permite asegurar que el dispositivo que quiere conectarse esta autenticado en el punto de acceso.

Posterior a este intercambio de claves, se procede a la generación de una clave privada denominada PMK(Pairwise Master Key), la cual es el resultado de pasar la contraseña a la función criptográfica PBKDF2-SHA1. Cuando nos encontramos en una Pre-Shared-Key Network la PMK (Pairwise Master Key) y PSK (Pairwise Transient Key) coinciden.

#### Four-Way Handsake

El protocolo Four-Way Handsake fue ideado con la intención de que el AP (Access Point) y el cliente puedan probar que conocen las claves PSK/PMK sin necesidad de revelar dicha clave. Para poder realizar esto el AP y el cliente encriptan los mensajes y se los envían al otro (dichos mensajes se pueden desencriptar con la PMK), si se logra desencriptarlos correctamente se demuestra que tienen conocimiento de la PSK.

Four-Way Handsake usa una PTK(Pairwise Transient Key), la cual esta compuesta por una combinanción de :

* PMK
* AP nonce (ANonce) y STA nonce (SNonce)
* AP Mac
* STA Mac

El producto de estos valores introducido en una función pseudoaleatoria tiene como resultado la PTK. El Handsake contiene también la GTK (Group Temporal Key), la cual es usada para desencriptar el tráfico de multicast y broadcast.

![Four-Way Handsake](img/4-way-handshake.png)

1. El AP envía un paquete Anonce (el cual contiene un valor que solo puede ser usado una vez en una función criptográfica) y un Key Replay Counter encargado de llevar la cuenta de los paquetes que se han transmitido.

2. El cliente (STA) responde con SNonce junto con un MIC (Message Integrity code), el cual incluye aunteticación, por lo tanto es un MAIC (Message Authentication Integrity Code) y el Key Replay Counter

3. El AP comprueba si el mensaje 2 es correcto mediante los campos MIC, Key Replay Counter, MIC, Anonce y RSN. Si el mensaje es correcto pasará a generar la GTK con otro MIC.

4. El STA verifica los datos del mensaje 3 y si es válido envía confirmación al AP.

Este protocolo es vulnerable a KRACK, la cual fue parcheda adecuadamente. Sin embargo, se observaba que en 2018 existían dispositivos sin actualizar que podian ser vulnerables.



### Wifi Protected Setup (WPS)

Es un protocolo fue implementado en 2006 con la finalidad de que aquellos usuarios que carezcan de conocimintos sobre seguridad en redes wifi, tengan la opción de crear una conexión segura y agregar nuevos dispositivos a una red existente. Para poder realizar estas acciones se implementaron 4 modos:

1. Método Pin: Este método consiste en introducir en el dispositivo un pin leido de una pegatina o pantalla en el dispositivo.
2. Presionando el botón: Este método consiste en presionar en ambos dispositivos (AP y STA) el botón de conexión, de forma que se active el modo de descubrimiento enlazando ambos dispositivos.
3. NFC 
4. USB

El método 3 y 4 se obvia la explicación puesto que han quedado completamente desactualizados.

#### ¿Como funciona el protocolo?

El protocolo consiste en un intercambio de mensajes EAP (Extensible Authentication Protocol), los cuales estan causados por una accion del usuario (confiando en una información previa). Esta información (WPS PIN) es intercambiada mediante un nuevo elemento de información (IE) que es agregado al beacon, probe response y opcionalmente al probe request y mensajes de petición/respuesta de asociación.

Tras esta comunicación entre los dispositivos el dispositivo comienza un protocolo de sesión. Esta sesión consiste en 8 mensajes que son seguidos (en caso de completarse satisfactoriamente) por un mensaje que indica que el procolo se ha completado correctamente.

#### Vulnerabilidades

* Online brute-force Attack: Este ataque consiste en realizar fuerza bruta al PIN del dispositivo, de forma que al obtenerlo se puede obtener la clave WPA. 

* Offline brute-force Attack: Esta ataque afecta a las implementaciones por defecto de algunos fabricantes. Consiste en obtener E-S1 y E-S2 nonces de forma que un fallo en la generación aleatoria de los mismos permite obtener el pin en un par de minutos. Este ataque es conocido como _pixiwps_

* Physical Security Issues: Cualquier fallo de seguridad puede ser extraído del router este no se encuentra en un lugar seguro.

!!!info
    Es recomendable desactivar el WPS, debido a que supone uno de los principales factores de ataque frente a un punto de acceso.