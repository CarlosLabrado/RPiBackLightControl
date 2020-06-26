from rpi_backlight import Backlight
import time
import pendulum
import requests


class BackLightControl:
    wake_time = None
    sleep_time = None
    last_check = None

    def __init__(self):
        print('initializing back light program...', flush=True)
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
            # self.sleep_time = el_paso_sunset.subtract(hours=4)

            print('Waking at {0}'.format(self.wake_time.to_day_datetime_string()), flush=True)

            print('Sleeping at {0}'.format(self.sleep_time.to_day_datetime_string()), flush=True)
        except Exception as e:
            print('there was an error getting the sunrise from the api: {0}'.format(e), flush=True)

    def main_app(self):

        while True:

            bl = Backlight()

            now = pendulum.now()
            print('Current time is {0}'.format(now.to_day_datetime_string()), flush=True)

            difference = now.diff(self.last_check, False).in_hours()

            if difference > 10:
                self.check_for_sunset_sunrise(day=now)

            hour = now.hour
            seconds_to_sleep = 600
            if (now > self.wake_time) and (now < self.sleep_time):
                print('It\'s time to wake up!', flush=True)
                bl.power = True
                bl.brightness = 50
                # lets always sleep 10 minutes instead
                # seconds_to_sleep = self.calculate_sleep_time_in_seconds(now_time=now, later_time=self.sleep_time)
                print('program sleeping for {0} minutes'.format(seconds_to_sleep / 60), flush=True)

            elif now >= self.sleep_time:
                print('Night time!', flush=True)
                self.decrease_brightness(hour, 22)
                # we check for tomorrow instead of today
                self.check_for_sunset_sunrise(day=now.add(days=1))
                # lets always sleep 10 minutes instead
                # seconds_to_sleep = self.calculate_sleep_time_in_seconds(now_time=now, later_time=self.wake_time)
            print('Sleeping {0} seconds'.format(seconds_to_sleep), flush=True)
            time.sleep(seconds_to_sleep)

    def calculate_sleep_time_in_seconds(self, now_time, later_time):
        minutes_to_sleep = now_time.diff(later_time, False).in_minutes()
        return minutes_to_sleep * 60

    def decrease_brightness(self, start_hour, finish_hour):
        print('start hour {}'.format(start_hour), flush=True)
        print('finish hour {}'.format(finish_hour), flush=True)
        print('decreasing brightness', flush=True)

        if finish_hour > start_hour:
            bl = Backlight()
            is_on = bl.power

            diff = finish_hour - start_hour

            half_hour_diff = diff * 2

            if is_on:
                print('is on', flush=True)
                brightness = 50
                for x in range(half_hour_diff):
                    print('brightness at {}'.format(brightness), flush=True)
                    if brightness < 10:
                        bl.power = False  # turn off the display
                    else:
                        if brightness == 10:
                            brightness = 11  # 11 is the min brightness
                        with bl.fade(duration=3):
                            bl.brightness = brightness
                        # bl.set_brightness(brightness, smooth=True, duration=3)
                        brightness = brightness - 10
                        print('sleeping 30 minutes...', flush=True)
                        time.sleep(60 * 30)

        else:
            raise Exception('the finish hour should be bigger than the start hour')


back_light_control = BackLightControl()
back_light_control.main_app()
