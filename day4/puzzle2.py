def asleepMostAtMinute(guards):
    maxMinuteFreq = 0
    maxGuard = None
    for guard in guards:
        guardMaxMinute = guard.getMaxMinute()
        if guard.sleepingMinutes[guardMaxMinute] > maxMinuteFreq:
            maxMinuteFreq = guard.sleepingMinutes[guardMaxMinute]
            maxGuard = guard
    return maxGuard
