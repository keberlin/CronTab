import re
import sys

MONTHS = {
    "1": "January",
    "2": "February",
    "3": "March",
    "4": "April",
    "5": "May",
    "6": "June",
    "7": "July",
    "8": "August",
    "9": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}

WEEKDAYS = {
    "0": "Sunday",
    "1": "Monday",
    "2": "Tuesday",
    "3": "Wednesday",
    "4": "Thursday",
    "5": "Friday",
    "6": "Saturday",
    "7": "Sunday",
    "sun": "Sunday",
    "mon": "Monday",
    "tue": "Tuesday",
    "wed": "Wednesday",
    "thu": "Thursday",
    "fri": "Friday",
    "sat": "Saturday",
}


def nth(v: str):
    if v == "1":
        return "1st"
    if v == "2":
        return "2nd"
    if v == "3":
        return "3rd"
    return f"{v}th"


class CrontabDescription:
    def __init__(self, schedule: str):
        self.every = False
        self.schedule = schedule

    def minutes_desc(self, v: str, hour: str):
        def fmt(v: str):
            return f"{int(hour):02d}:{int(v):02d}" if hour is not None else f"{int(v):02d}"

        r = v.split("/")
        if len(r) > 1:
            assert len(r) == 2
            self.every = True
            return f"every {r[1]} minutes " + self.minutes_desc(r[0], hour)

        r = v.split("-")
        if len(r) > 1:
            assert len(r) == 2
            self.every = True
            return f"between minutes {r[0]} to {r[1]}"

        if v == "*":
            ret = "every minute" if not self.every else ""
            self.every = True
            return ret

        ret = " and ".join([fmt(x) for x in v.split(",")])
        if hour is None:
            ret += " minutes past"
        return ret

    def hour_desc(self, v: str):
        r = v.split("/")
        if len(r) > 1:
            assert len(r) == 2
            return f"every {nth(r[1])} hour " + self.hour_desc(r[0])

        r = v.split("-")
        if len(r) > 1:
            assert len(r) == 2
            return "from " + self.hour_desc(r[0]) + " to " + self.hour_desc(r[1])

        if v == "*":
            ret = "every hour" if not self.every else ""
            self.every = True
            return ret
        return f"{int(v):02d}"

    def hours_desc(self, v: str):
        ret = " and ".join([self.hour_desc(x) for x in v.split(",")])
        return ret

    def day_desc(self, v: str):
        r = v.split("-")
        if len(r) > 1:
            assert len(r) == 2
            return self.day_desc(r[0]) + " to " + self.day_desc(r[1])

        if v == "*":
            ret = "every day" if not self.every else ""
            self.every = True
            return ret
        return nth(v) if v != "*" else ""

    def days_desc(self, v: str):
        ret = ",".join([self.day_desc(x) for x in v.split(",")])
        return "on the " + ret + " of" if ret else ""

    def month_desc(self, v: str):
        r = v.split("-")
        if len(r) > 1:
            assert len(r) == 2
            return self.month_desc(r[0]) + " to " + self.month_desc(r[1])

        if v == "*":
            ret = "every month" if not self.every else ""
            self.every = True
            return ret
        return MONTHS[v.lower()]

    def months_desc(self, v: str):
        ret = ",".join([self.month_desc(x) for x in v.split(",")])
        return "in " + ret if ret else ""

    def weekday_desc(self, v: str):
        r = v.split("-")
        if len(r) > 1:
            return self.weekday_desc(r[0]) + " to " + self.weekday_desc(r[1])

        if v == "*":
            return ""
        return WEEKDAYS[v.lower()]

    def weekdays_desc(self, v: str):
        ret = " and ".join([self.weekday_desc(x) for x in v.split(",")])
        return "on " + ret if ret else ""

    def desc(self):
        schedules = self.schedule.split()
        if len(schedules) < 5:
            return None

        minutes = schedules[0]
        hours = schedules[1]
        days = schedules[2]
        months = schedules[3]
        weekdays = schedules[4]
        # print(f"minutes: {minutes}, hours: {hours}, days: {days}, months: {months}, weekdays: {weekdays}")

        desc = []
        try:
            prefix = int(hours)
        except:
            prefix = None
        desc.append(self.minutes_desc(minutes, prefix))
        if prefix is None:
            desc.append(self.hours_desc(hours))
        desc.append(self.days_desc(days))
        desc.append(self.weekdays_desc(weekdays))
        desc.append(self.months_desc(months))

        # Convert into a single line of text
        desc = " ".join(list(filter(None, desc)))

        # Tidy up the English text
        desc = re.sub(r"0([0-9] minutes past)", r"\1", desc)
        desc = re.sub(r"on the every day of", r"every day", desc)
        desc = re.sub(r"every day on", r"on", desc)
        desc = re.sub(r"in every month", r"every month", desc)

        if not desc.startswith("every") and not desc.startswith("between"):
            desc = "at " + desc

        desc = desc[0].upper() + desc[1:]

        return desc


if __name__ == "__main__":
    f = sys.stdin
    lines = f.readlines()
    for line in lines:
        if line.startswith("#") or line.startswith("@"):
            continue

        parts = line.split()
        if len(parts) < 6:
            continue

        schedule = " ".join(parts[0:5])
        command = " ".join(parts[5:])

        description = CrontabDescription(schedule).desc()

        if command.startswith("cronitor exec"):
            parts = command.split()
            cronitor = parts[2]
            command = " ".join(parts[3:])
        else:
            cronitor = ""

        print(f"{schedule}; {description}; {cronitor}; {command}")
