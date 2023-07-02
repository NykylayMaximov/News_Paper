import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def send_mail_weekly_posts():
    post_weekly = datetime.now() - timedelta(days=7)
    posts = Post.objects.filter(time__gte=post_weekly)
    categories = set(posts.values_list('categories__category', flat=True))
    subscribers = set(Category.objects.filter(category__in=categories).values_list('subscribers__email', flat=True))
    subscribers_list = []
    for sub in subscribers:
        if sub is not None:
            subscribers_list.append(sub)

    html_content = render_to_string('post_weekly_send_email.html', {'posts': posts})
    msg = EmailMultiAlternatives(
        subject='Уруй Айхал! Сборка новостей за неделю',
        from_email='nick.max89@gmail.com',
        to=subscribers_list,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print('отпрвил')


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_mail_weekly_posts,
            trigger=CronTrigger(day_of_week='mon'),
            id="send_mail_weekly_posts",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")