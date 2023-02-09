## uses

https://github.com/linusg/rpi-backlight

## issues

The sunrise API started to fail after raspbian upgrade, apparently the random generator stopped working. had to install

```angular2html
 sudo apt-get install haveged
```

That is a random generator that doesn't need the mouse? because there's not enough entropy?? :S

### Cron tab

Install the package.whl using pip on the terminal

sudo crontab -e

```shell script
@reboot /usr/bin/env python /home/pi/.local/bin/backlight_start >> /home/pi/backlight_control/my.log 2>&1
```

# New Setup

- Install poetry
  ** There's an issue when running poetry install through SSH
  - [1917](https://github.com/python-poetry/poetry/issues/1917)
  - Fix
    - ```shell
      echo 'export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring' >> ~/.bashrc
      echo 'export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring' >> ~/.profile
      exec "$SHELL"
      ```

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

# Systemd

We need to create a `.service` file with:
```shell
sudo nano /etc/systemd/system/light_control.service
```

Place this code inside it:
```
[Unit]
Description=Backlight control

[Service]
ExecStart=/usr/bin/bash -c "./run.sh"
User=pi
WorkingDirectory=/home/pi/backlight_control

[Install]
WantedBy=multi-user.target
```

Then run these commands to enable it:
```shell
sudo systemctl enable light_control.service

sudo systemctl start light_control.service

systemctl status light_control.service
```

