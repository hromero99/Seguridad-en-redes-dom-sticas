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

### Activando el modo monitor: airmon-ng

Una vez comprobado si la tarjeta es compatible, pasaremos a ponerla el modo monitor. 

```Aircrack-ng requiere ser ejecutado como root```
```  Para los ejemplos de comandos se utilizará la interfaz wlan0, esto debe de ser cambiado según la interfaz```


    $ root@HowIsCoding:~$  airmon-ng check wlan0

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

    $ airmon-ng check kill

Cuando tenemos los procesos que entraban en conflicto matados podemos pasar a poner la interfaz en modo monitor, para ello usaremos la misma herramienta:

    $ airmon-ng start wlan0

    PHY	Interface	Driver		Chipset

    phy0	wlan0		ath9k_htc	Atheros Communications, Inc. AR9271 802.11n

		(mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
		(mac80211 station mode vif disabled for [phy0]wlan0)

Como podemos ver en la salida del comando airmon-ng se ha habilitado el modo monitor de nuestra tarjeta. Para operar con el momo monitor se habilita la interfaz wlan0mon.

Podemos comprobar los canales Wifi en los que esta ecuchando nuestra tarjeta en modo monitor, para ello podemos usar el comando:
    
    $ iwlist wlan0mon channel

Cuando hemos encontrado la red que queremos auditar (como se explicará en el siguiente apartado), podemos suministrar el canal como argumento opcional a airmon-ng, de la siguiente forma:

    $ airmon-ng start wlan0 3



Al igual que podemos poner la tarjeta en modo monitor, cuando terminemos de trabajar con ella debemos desactivarla, para ello airmon-ng nos permite desactivarlo haciendo uso del comando:
    
    $ airmon-ng stop wlan0


## Escaneando redes wifi: airmon-ng

Una vez con nuestra interfaz en modo monitor pasaremos a realizar un escaneo de todas las redes wifi que estan en nuestro entorno, para ello utilizaremos la herramienta _airodump-ng_

    $ airodump-ng wlan0mon

        CH  2 ][ Elapsed: 36 s ][ 2019-01-07 14:58                                         
                                                                                                                                                                
    BSSID              PWR  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID
                                                                                                                                                                
    00:14:5C:84:4D:42  -44       14        5    1   6  54 . WPA2 TKIP   PSK  wireless.py                                                                        
    48:8D:36:BC:25:A2  -63       14        3    0   1  130  WPA2 CCMP   PSK  Orange-25A0                                                                        
                                                                                                                                                                
    BSSID              STATION            PWR   Rate    Lost    Frames  Probe                                                                                   
                                                                                                                                                                
    48:8D:36:BC:25:A2  10:00:00:8A:95:26  -21    0 - 6e     0        4                                                                                           
``` La terminología usada en el resultado de este comando esta explicada en el apartado anterior``
Es necesario examinar el resultado de esta herramienta y explicar a groso modo su funcionamiento.

Airodump-ng realizará un escaneo por todos los canales de radio referentes a las redes wifi, buscando las diferentes señales (ya que permite capturar paquetes mediante el modo monitor). También detecta los clientes que existen en esas redes, así como sus direcciones mac y los puntos de acceso a los que están conectados.

Con este resultado podemos enfocarnos en un determinado punto de acceso, sin embargo, podemos realizar una captura de todo el tráfico y almacenarla en un archivo _pcap_ para su posterior análisis con _Wireshark_ u otra herramienta.

### Capturando paquetes del objetivo

Una vez hemos identificado los datos de la red objetivo, pasaremos a capturar información sobre ese punto en concreto (obviando el resto de redes).

    $ airodump-ng --bssid 00:14:5C:84:4D:42 --essid wireless.py -c 6 -w wirelessPY wlan0mon

Este comando nos dará como resultado un paquete _cap_(wirelessPY.cap) para analizar posteriormente.

