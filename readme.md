## uses

https://github.com/linusg/rpi-backlight

## issues

The sunrise API started to fail after raspbian upgrade, apparently the random generator stopped working. had to install

```angular2html
 sudo apt-get install haveged
```

That is a random generator that doesn't need the mouse? because there's not enough entropy?? :S

### Cron tab

sudo crontab -e

```shell script
@reboot python3 /home/pi/BackLightPy/test.py >> /home/pi/BackLightPy/my.log 2>&1
```

Install poetry
%APPDATA%\Python\Scripts

```shell

```