# Vulnerabilidades en redes wifi

Como se ha detallado en el apartado anterior encontramos diferentes aspectos dentro de una red wifi que deben de ser analizados. Para realizar análisis de redes wifi disponemos de la suite [**Aircrack-ng**](https://www.aircrack-ng.org/), la cual nos brinda numerosas herramientas para poder realizar dicho análisis.

## ¿Qué es el modo monitor?

Antes de entrar en materia, es necesario introducir un concepto nuevo en el ámbito de las redes wifi: _monitor mode_. Haciendo una simple búsqueda en Wikipedia encontramos:

```Monitor mode, or RFMON (Radio Frequency MONitor) mode, allows a computer with a wireless network interface controller (WNIC) to monitor all traffic received on a wireless channel. Unlike promiscuous mode, which is also used for packet sniffing, monitor mode allows packets to be captured without having to associate with an access point or ad hoc network first```

Traduciendo al español (la parte que nos interesa) concluimos que el modo monitor nos permite capturar paquetes sin necesidad de estar asociado a un punto de acceso. Esta funcionalidad que nos permiten determinadas chips de tarjetas wifi será esencial para analizar las diferentes redes de nuestro entorno.

### ¿Cómo comprobar si la tarjeta es compatible?

Una vez que ha quedado claro que es el modo monitor y para que sirve, se recomienda __utilizar tarjetas externas__ por dos razones principales:

*   El chipset de las tarjetas externas brindan mejor soporte para modo monitor.
*   La tarjeta wifi interna puede ser dañada debido al procesamiento de paquetes.

Dicho esto, lo primero que tenemos que realizar sería comprobar que tenemos una tarjeta que soporte el modo monitor, para ello utilizaremos el siguiente comando:

        $ iw list 
    
Dentro de la salida extensa de este comando tenemos la categoria _Supported interface modes_ donde podemos comprobar si se incluye el modo monitor.

### Activando el modo monitor

Una vez comprobado si la tarjeta es compatible, pasaremos a ponerla el modo monitor. 

```Aircrack-ng requiere ser ejecutado como root```
```  Para los ejemplos de comandos se utilizará la interfaz wlp3s0, esto debe de ser cambiado según la interfaz```


    $ root@HowIsCoding:~$  airmon-ng check wlp3s0

    Found 5 processes that could cause trouble.
    Kill them using 'airmon-ng check kill' before putting
    the card in monitor mode, they will interfere by changing channels
    and sometimes putting the interface back in managed mode

    PID Name
    5771 dhclient
    7888 wpa_supplicant
    8878 NetworkManager
    9214 avahi-daemon
    9225 avahi-daemon

Antes de poner la interfaz en modo monitor debemos de realizar una comprobación en busca de procesos (como el network Manager) que esten utilizando la interfaz, de forma que tendremos que matarlos. Si dejamos estos procesos corriendo pueden realizar acciones como cambiar la antena de canal o impedirla trabajar el modo monitor. 

Para matar estos procesos simplemente usamos la herramienta airmon-ng para matarlos:

    $ airmon-ng kill wlp3s0

Cuando tenemos los procesos que entraban en conflicto matados podemos pasar a poner la interfaz en modo monitor, para ello usaremos la misma herramienta:

    $ airmon-ng start wlp3s0

