from django.utils import timezone


class TimeClass:
    def get_nowtime(self):
        return timezone.now()

tc = TimeClass()
