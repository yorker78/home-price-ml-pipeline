import datetime as dt

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from cleaning_job import check_environment, run_job

if __name__ == "__main__":
    environment = check_environment()
    match(environment):
        case 0:
            scheduler = BlockingScheduler()
            scheduler.add_job(func=run_job, trigger=IntervalTrigger(minutes=15), max_instances=1, coalesce=True)
            for job in scheduler.get_jobs():
                job.modify(next_run_time=dt.datetime.now())
            scheduler.start()
        case 1:
            print('DB_USER is not set')
        case 2:
            print('DB_PASS is not set')
        case 3:
            print('DB_HOST is not set')
        case 4:
            print('DB_USER is not set')
            print('DB_PASS is not set')
        case 5:
            print('DB_USER is not set')
            print('DB_HOST is not set')
        case 6:
            print('DB_PASS is not set')
            print('DB_HOST is not set')
        case 7:
            print('DB_USER is not set')
            print('DB_PASS is not set')
            print('DB_HOST is not set')
        case _:
            print('Significant Error Has Occurred While Obtaining Environment Variables')