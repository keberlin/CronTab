from crontab import CrontabDescription


def test_every_minute():
    result = CrontabDescription("* * * * *").desc()
    assert result == "Every minute"

    result = CrontabDescription("*/10 * * * *").desc()
    assert result == "Every 10 minutes"

    result = CrontabDescription("1,5 5 * * 1-6").desc()
    assert result == "At 05:01 and 05:05 on Monday to Saturday"

    result = CrontabDescription("0 * * * *").desc()
    assert result == "At 0 minutes past every hour"

    result = CrontabDescription("0 0 * * *").desc()
    assert result == "At 00:00 every day"

    result = CrontabDescription("0 0 * * 0").desc()
    assert result == "At 00:00 on Sunday"

    result = CrontabDescription("0 19,20 * * *").desc()
    assert result == "At 0 minutes past 19 and 20 every day"

    result = CrontabDescription("0 0 2 * *").desc()
    assert result == "At 00:00 on the 2nd of every month"

    result = CrontabDescription("30 10 * * *").desc()
    assert result == "At 10:30 every day"

    result = CrontabDescription("0 0 * * 6,0").desc()
    assert result == "At 00:00 on Saturday and Sunday"

    result = CrontabDescription("5 0 * 8 *").desc()
    assert result == "At 00:05 every day in August"

    result = CrontabDescription("15 14 1 * *").desc()
    assert result == "At 14:15 on the 1st of every month"

    result = CrontabDescription("0 22 * * 1-5").desc()
    assert result == "At 22:00 on Monday to Friday"

    result = CrontabDescription("23 0-20/2 * * *").desc()
    assert result == "At 23 minutes past every 2nd hour from 00 to 20 every day"

    result = CrontabDescription("5 4 * * sun").desc()
    assert result == "At 04:05 on Sunday"
