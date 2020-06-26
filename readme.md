## uses
https://github.com/linusg/rpi-backlight

### Cron tab
sudo crontab -e
```shell script
@reboot python3 /home/pi/BackLightPy/test.py >> /home/pi/BackLightPy/my.log 2>&1
```
