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

# New Setup

- Install poetry

#### Settings for RPI 7inch screen

- Install PIPx

- Settings for RPI backlight
    ```shell
    echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/ba cklight-permissions.rules
    ```
- Install [PiHole](https://pi-hole.net/)
- Screen Settings for [PAAD](https://github.com/pi-hole/PADD)

  `sudo dpkg-reconfigure console-setup`

  - UTF-8
  - Guess Optimal Character
  - Terminus
  - 10x18