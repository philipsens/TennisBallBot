# TennisBallBot

## Installation 

### Raspberry pi

* Update the rapsberry pi's code bij executing the following two lines.

```
sudo apt update
sudo apt full-upgrade
```

* Enable the pi cam by running `sudo raspi-config`, and go to the promp in _Interfacing Options > Camera_. And reboot.

* Execute `./raspberry/install_dependencies.sh`.

* Change workdir to the webapp folder `cd raspberry/webserver/webapp`.

* Create an environment file `cp .env.example .env.local`.

* Fill in the api uri, this should be the ip of the `http://` + raspberry pi + `/api/` note the trailing slash.

* Execute `npm install && npm run build`.