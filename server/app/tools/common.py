from django.utils import timezone


class TimeClass:
    def get_nowtime(self):
        return timezone.now().strftime('%Y-%m-%d %H:%M:%S')

tc = TimeClass()