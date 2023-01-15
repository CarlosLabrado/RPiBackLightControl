from typing import Optional

from rpi_backlight import Backlight
import time
import pendulum
import requests


class BackLightControl:
    wake_time = None
    sleep_time = None
    last_check = None
    backlight = None

    def __init__(self, backlight: Optional = None):
        print('initializing back light program...', flush=True)
        self.backlight = backlight or Backlight()
        now = pendulum.now()
        self.check_for_sunset_sunrise(day=now)

    def check_for_sunset_sunrise(self, day):

        try:
            print('checking for sunset/sunrise')
            time.sleep(30)
            now = pendulum.now()
            self.last_check = now

            day_to_request = day.format('YYYY-MM-DD')

            # from https://sunrise-sunset.org/api
            api_request = requests.get(
                'https://api.sunrise-sunset.org/json?lat=31.7795127&lng=-106.4846813&date={0}&formatted=0'
                .format(day_to_request)
            )
            json_api = api_request.json()
            sunset = json_api['results']['sunset']
            sunrise = json_api['results']['sunrise']

            utc_sunset = pendulum.parse(sunset)
            utc_sunrise = pendulum.parse(sunrise)

            el_paso_sunset = utc_sunset.in_timezone('America/Denver')
            el_paso_sunrise = utc_sunrise.in_timezone('America/Denver')

            self.wake_time = el_paso_sunrise.add(hours=1)
            self.sleep_time = el_paso_sunset.subtract(minutes=45)

            print('Waking at {0}'.format(self.wake_time.to_day_datetime_string()), flush=True)

            print('Sleeping at {0}'.format(self.sleep_time.to_day_datetime_string()), flush=True)
        except Exception as e:
            print('there was an error getting the sunrise from the api: {0}'.format(e), flush=True)

    def main_app(self) -> bool:

        try:

            now = pendulum.now()
            print('Current time is {0}'.format(now.to_day_datetime_string()), flush=True)

            difference = now.diff(self.last_check, False).in_hours()

            if difference > 10:
                self.check_for_sunset_sunrise(day=now)

            hour = now.hour
            if self.wake_time and self.sleep_time:
                if (now > self.wake_time) and (now < self.sleep_time):
                    print('It\'s time to wake up!', flush=True)
                    self.backlight.power = True
                    self.backlight.brightness = 50
                elif now >= self.sleep_time:
                    print('Night time!', flush=True)
                    self.decrease_brightness(hour, 22)
                    # we check for tomorrow instead of today
                    self.check_for_sunset_sunrise(day=now.add(days=1))

                return True  # sleep
            else:
                # re-initialize because times are NONE
                self.check_for_sunset_sunrise(day=now)
                return False  # don't sleep

        except Exception as e:
            print('Error running main_app : {0}'.format(e))

    @staticmethod
    def calculate_sleep_time_in_seconds(now_time, later_time):
        minutes_to_sleep = now_time.diff(later_time, False).in_minutes()
        return minutes_to_sleep * 60

    def decrease_brightness(self, start_hour, finish_hour):
        print('start hour {}'.format(start_hour), flush=True)
        print('finish hour {}'.format(finish_hour), flush=True)
        print('decreasing brightness', flush=True)

        if finish_hour > start_hour:
            is_on = self.backlight.power

            diff = finish_hour - start_hour

            half_hour_diff = diff * 2

            if is_on:
                print('is on', flush=True)
                brightness = 50
                for x in range(half_hour_diff):
                    print('brightness at {}'.format(brightness), flush=True)
                    if brightness < 10:
                        self.backlight.power = False  # turn off the display
                    else:
                        if brightness == 10:
                            brightness = 11  # 11 is the min brightness
                        with self.backlight.fade(duration=3):
                            self.backlight.brightness = brightness
                        # bl.set_brightness(brightness, smooth=True, duration=3)
                        brightness = brightness - 10
                        print('sleeping 30 minutes...', flush=True)
                        time.sleep(60 * 30)
        elif finish_hour == start_hour:
            self.backlight.power = False
        else:
            raise Exception('the finish hour should be bigger than the start hour')


def main():
    back_light_control = BackLightControl()
    while True:
        seconds_to_sleep = 600

        should_sleep = back_light_control.main_app()
        if should_sleep:
            # let's always sleep 10 minutes instead
            print('Sleeping {0} seconds'.format(seconds_to_sleep), flush=True)
            time.sleep(seconds_to_sleep)


if __name__ == '__main__':
    main()
