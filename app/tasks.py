import logging
from .data_retrieval import store_metrics

logger = logging.getLogger(__name__)

def schedule_logging(scheduler):
    """ configures the job being scheduled """
    scheduler.add_job(
        id='collect_metrics',
        func=store_metrics,
        trigger='interval',
        minutes=10,
        replace_existing=True
    )
    logger.info("Scheduled metrics collection job")
