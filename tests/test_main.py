import unittest
from unittest.mock import Mock

import pendulum

from src.custom_control.main import BackLightControl


class MockBackLight:
    pass


class SomeFncTestCase(unittest.TestCase):

    @unittest.mock.patch('src.custom_control.main.BackLightControl.backlight')
    def test_control(self, m):
        back_light_control = BackLightControl(backlight=m)
        back_light_control.main_app()
