# Ataques en la red interna 

Una vez que estamos dentro de la red wifi, nos encontramos ante un escenario totalmente diferente al anterior. Tenemos que realizar descubrimiento de equipos, comprobar configuraciones por defecto, explorar vulnerabilidades del hardware de red, entre una larga lista de tareas. Dicho esto comencemos por el primer paso: _descubrimiento de objetivos_

## Descubrimiento de dispositivos

Teniendo en cuanta las características estándar de una red cuyo hardware de red está suministado por el ISP (Internet Service Provider) y asumiendo configuraciones por defecto existirá un servidor DHCP (Dynamic Host Configuration Protocol) el cual automáticamente nos asignirá los datos necesarios para tener acceso a internet.

Al obtener una dirección ip automáticamente (como consecuencia del servidor DHCP), podremos tener cierta idea del tipo de red en el que estamos trabajando y en consecuncia realizar un escaneo de los dispositivos existentes.

El primer paso sería obtener determinada información de la red, para ello podemos utilizar las herramientas que nos proporiciona nuestro sistema GNU/Linux, concretamente  _route_

    $ route 

    Kernel IP routing table
    Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
    default         10.0.2.1        0.0.0.0         UG    100    0        0 wlan0
    10.0.2.0        0.0.0.0         255.255.255.0   U     100    0        0 wlan0


Generalmente el comando _route_ nos mostrará algo similar a lo anterior. Dentro de esta salida nos permite obtener cierta información:

* Puerta de enlace (Gateway): Esta dirección nos permitirá saber mediante que dispositivo estamos saliendo a Internet
* Máscara de red: Nos permitirá determinar en que tipo de red estamos trabajando (Tipo A,B,C)
 
Esta información nos permitirá posteriormente realizar un escaneo de la red en busca de dispositivos.

### Protocolo ARP

Para realizar el descubrimiento de los equipos disponibles en la red usaremos la herramienta _nmap_ puesto que nos permite obtener gran cantidad de información dentro de una red. En primer lugar, realizaremos un escaneo ARP (debido a su velocidad) para enumerar los dispositivos existentes:

    $ nmap -sn 10.0.2.0/24
    Starting Nmap 7.70 ( https://nmap.org ) at 2019-01-09 18:55 CET
    Nmap scan report for 10.0.2.1
    Host is up (0.00032s latency).
    MAC Address: 52:54:00:12:35:00 (QEMU virtual NIC)
    Nmap scan report for 10.0.2.2
    Host is up (0.00019s latency).
    MAC Address: 52:54:00:12:35:00 (QEMU virtual NIC)
    Nmap scan report for 10.0.2.3
    Host is up (0.00020s latency).
    MAC Address: 08:00:27:8B:3F:6E (Oracle VirtualBox virtual NIC)
    Nmap scan report for 10.0.2.15
    Host is up (0.00039s latency).
    MAC Address: 08:00:27:7E:F5:47 (Oracle VirtualBox virtual NIC)
    Nmap scan report for 10.0.2.4
    Host is up.
    Nmap done: 256 IP addresses (5 hosts up) scanned in 7.61 seconds

El protocolo ARP (Address Resolution Protocol) es un protoclo que trabaja en la capa 2 de la [pila TCP/IP](https://simple.wikipedia.org/wiki/TCP/IP_model), este protocolo permite traducir las direcciones físicas (MAC) en direcciones lógicas (IP) que identifiquen nuestros dispositivos. Este traducción de direcciones es necesaria para operar posteriormente.

Esta información queda almacenada en nuestro sistema, de forma que podemos consultarla en cualquier momento haciendo uso de la herramienta _arp_

    $ arp -e 
    Address                  HWtype  HWaddress           Flags Mask            Iface
    10.0.2.1                 ether   52:54:00:12:35:00   C                     wlan0
    10.0.2.15                ether   08:00:27:7e:f5:47   C                     wlan0

Como podemos ver podemos consultar las direcciones físicas (HWaddress), relacionadas con cada dirección IP (Address). La información almacenada en esta tabla es esencial, puesto que cuando queremos enviar datos (paquetes) entre diferentes máquinas (nustra máquina local y un servidor web), se realizará mediante la dirección física, por lo que el sistema operativo consultará los datos almacenados en esta tabla.

#### ¿Qué sucede si no esta la dirección en la tabla ARP?

Cuando no encontramos una dirección en la tabla ARP, el sistema operativo envia un paquete ARP _request_ preguntando _Who has 10.0.2.15?_ hacia una dirección en concreto (dirección de broadcast), esto puede observarse examinando un paquete tipo request con Wirehark:

![Arp request](img/arpRequest1.png)

Como podemos ver la dirección de destino del paquete es la dirección de broadcast (ff:ff:ff:ff:ff:ff). Por parte del protocolo ARP, se envía la siguiente información.

![Arp request 2](img/arpRequest2.png)

Como se puede observar se indica la dirección ip destino, la dirección que queremos descubrir en la red.

En caso de que dicha dirección exista, tendrá una dirección MAC asociada, por lo cual el protolo ARP recibirá respuesta con un paquete ARP tipo _reply_ donde se encuentra la dirección física del dispositivo.

![Arp reply](img/arpReply1.png)

Si la dirección ip a la cual estamos enviando el paquete _request_ no se encuentra en la red, no obtenedremos respuesta por parte del protocolo ARP. 

Ententiendo como funciona el protocolo ARP, sería muy fácil llegar a la conclusión de que si enviamos paquetes a todas las direcciones posibles dentro de nuestra máscara de red, solo aquellas peticiones que tengan respuesta harán referencia a los dispositivos existentes en la red.

#### Problemas del escaneo ARP
El principal problema que plantea un escaneo de tipo ARP es que genera mucho ruido en la red, de forma que puede ser detectado facilmente por cualquier detector de intrusos. Sin embargo, en el escenario en el que estamos se supone que no existen dichos mecanismos.

__Como ejemplo del ruido generado en la red se deja a continuación un paquete .pcapg__ ![Análisis de Wirehark]()