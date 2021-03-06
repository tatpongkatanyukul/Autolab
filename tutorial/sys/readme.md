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

## Trace code

### Autolab
(1) The starting point is ```/home/autolab/Autolab/runrail.sh```
Contents of ```runrail.sh```
```
#!/usr/bin/env bash
RAILS_ENV=development bundle exec rails s -p 3000 -e development --binding=localhost${_reset}
```
Explanation
  * ```rails s``` or ```rails server``` is a command to start rails server.
  * ```-p 3000``` is to specify port to 3000.
    * if tested on a localhost, check out url: ```localhost:port```, e.g., ```localhost:3000``` 
    * default account for development version: ```admin@foo.bar```

See [Rails initialization for sequence of codes get run](https://guides.rubyonrails.org/initialization.html)

(2) At some point along with rails initialization, it will get to ```config/application.rb```
Part of the contents of ```application.rb```
```
module Autolab3
  class Application < Rails::Application
    config.to_prepare do
      Devise::ConfirmationsController.skip_before_action :set_course
      Devise::ConfirmationsController.skip_before_action :authorize_user_for_course
      Devise::ConfirmationsController.skip_before_action :authenticate_for_action
      Devise::ConfirmationsController.skip_before_action :update_persistent_announcements
        :              :                    :                    :
      Devise::SessionsController.layout "home"
      Devise::RegistrationsController.layout proc{ |controller| user_signed_in? ? "application"   : "h$
      Devise::ConfirmationsController.layout "home"
      Devise::UnlocksController.layout "home"
      Devise::PasswordsController.layout "home"
      Doorkeeper::AuthorizationsController.layout "home"
      Doorkeeper::AuthorizedApplicationsController.layout "home"
    end        
```
Key modules
  * ```config/application.rb```
  * ```config/routes.rb```
    * get
    * post
    * match
  * ```app/controllers/assessments_controller.rb```
    * see e.g., ```def index```
  * easy to start with: ```app/controllers/announcement_controller.rb```
    * also check out ```index.html.erb``` (template) and ```_announcementFields.html.erb``` 

(3) ruby: ```/home/autolab/.rbenv/versions/2.6.1/bin/ruby```

### Autograder 
See ```/home/autolab/Tango3/restful-tango/server``` and ```/home/autolab/Tango3/tango.py```
    
![Autolab](https://github.com/tatpongkatanyukul/Autolab/blob/main/tutorial/sys/Autolab_system.png)  
  
#### Test autograder on the server
  * 1 ssh (putty) into the autolab
  * 2 sftp (filezilla) into the autolab
  * 3 transfer files in to ```sandbox/<folder>```
  * 4 start docker ```docker run -v /home/tatpong/sandbox:/home/sandbox -it python39_image bash```
  * 5 go into ```sandbox/<folder>``` and extract the package
  * 6 try ```python3.9 dispatcher.py "./cfg/eval2021h.cfg" -autolab```
    * If it works, nothing's wrong with the autograder code. Check Tango (restart, maybe?)
    * If it does not work, fix it! 
  
## Web Server (NginX)
  * type ```nginx -V``` to see configuration
    *  found ```/usr/share/nginx/html/index.html```, but it is not what is shown on the default ip ```http://202.28.93.227/```
    *  found ```root /home/admin/Autolab/public``` on ```/etc/nginx/sites-available/autolab```
    *  found ```root /home/autolab/Autolab/public``` on ```/etc/nginx/sites-available/default```
  * I see, Nginx is not a file-based system, like Apache. It processes [URI](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier).
    * So, I may not see a html like I was expecting in the beginning. 
