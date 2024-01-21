import time
import threading

class scheduleService:
    def scheduleThreadLoop(interval, targetFunction):
        while True:
            targetFunction()
            # print(f"[i] Schedule: Executed {targetFunction.__name__}")
            time.sleep(interval)

    def runShedule(interval:int, targetFunction):
        scheduleThread = threading.Thread(target=scheduleService.scheduleThreadLoop, args=(interval, targetFunction))
        scheduleThread.daemon = True
        scheduleThread.start()