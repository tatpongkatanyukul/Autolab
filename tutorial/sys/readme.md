# Autolab Server

## Examine procedure

  * 1. ```ping autolab.en.kku.ac.th```
    * not respond ---> server is dead! (browser gets to nowhere)
    * respond
  * 2. Check each component
    * Get root previlege
      * ```sudo -s -H```
    * Check status
      * ```systemctl status nginx```
        * if nginx is dead, there is no web at all 
      * ```systemctl status Autolab```
        * if Autolab is dead, there is web, but no Autolab web, e.g., "Bad gateway" 
      * ```systemctl status Tango3-Server```
        * If Tango3 is dead, autograder does not work.
        * see Job (on Autolab website)
    * Try stop/start or restart
      * E.g., ```systemctl restart Tango3-Server```
  * 3. Check resource usage in the server
    * ```htop```
  * 4. Trace code
Autolab: ```/home/autolab/Autolab/runrail.sh``` (need Aj Wasu's confirmation)
Contents of ```runrail.sh```
```
#!/usr/bin/env bash
RAILS_ENV=development bundle exec rails s -p 3000 -e development --binding=localhost${_reset}
```
Autograder 
See ```/home/autolab/Tango3/restful-tango/server``` and ```/home/autolab/Tango3/tango.py```
    
![Autolab](https://github.com/tatpongkatanyukul/Autolab/blob/main/tutorial/sys/Autolab_system.png)  
  
