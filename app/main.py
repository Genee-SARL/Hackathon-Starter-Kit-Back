from shared import create_app
import os
from dotenv import load_dotenv

from config import TestingConfig, ProductionConfig, DevelopmentConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from manager.scraper import ScraperManager
import pytz
import threading


load_dotenv()

match os.getenv('ENV'):
    case 'dev':
        config = DevelopmentConfig()
    case 'prod':
        config = ProductionConfig()
    case 'test':
        config = TestingConfig()
    case _:
        config = DevelopmentConfig()

print(f"Using environment {config.ENV}")

app = create_app(config)

scheduler = BackgroundScheduler()
paris_tz = pytz.timezone('Europe/Paris')
scraper_manager = ScraperManager()
def stop_scheduler():
    get_position_scheduler.pause()
    get_equity_scheduler.pause()


def resume_scheduler():
    get_position_scheduler.resume()
    get_equity_scheduler.resume()


get_position_scheduler = scheduler.add_job(scraper_manager.check_traders_position,
                                           trigger=CronTrigger(second='*/15',minute='*',hour='*',day_of_week='mon-thu'),
                                           max_instances=1,timezone=paris_tz)
get_equity_scheduler = scheduler.add_job(scraper_manager.get_trader_drowdown,'cron',hour=1,minute=0,second=0,
                                         day_of_week='mon-fri',timezone=paris_tz)
scheduler.add_job(stop_scheduler,'cron',day_of_week='fri',hour=23,minute=0,second=0,timezone=paris_tz)
scheduler.add_job(resume_scheduler,'cron',day_of_week='sun',hour=23,minute=0,second=0,timezone=paris_tz)

scheduler_thread = threading.Thread(target=scheduler.start)
scheduler_thread.start()
scheduler_thread.join()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001", debug=True)
