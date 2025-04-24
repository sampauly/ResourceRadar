import logging
from .data_retrieval import store_metrics, scheduler

logger = logging.getLogger(__name__)

def schedule_logging(scheduler):
    """ configures the job being scheduled """
    scheduler.add_job(
        id='collect_metrics',
        func=store_metrics,
        trigger='interval',
        minutes=1,
        replace_existing=True
    )
    logger.info("Scheduled metrics collection job")