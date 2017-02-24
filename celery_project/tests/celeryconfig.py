# coding=utf-8
from celery.schedules import crontab
from kombu import Exchange
from kombu import Queue

# 延迟acks
task_acks_late = True
task_reject_on_worker_lost = True

timezone = 'Asia/Shanghai'
enable_utc = True
# broker_url = 'redis://localhost:6379/0'
broker_url = 'amqp://mx_rabbit:mx_rabbit@localhost:5672/mx_vhost'
result_backend = 'redis://localhost:6379/0'

# 麦享 默认队列设置
mx_default_queue_name = 'default_queue'
mx_default_routing_key = 'default.route_key'

# 默认设置
task_default_queue = mx_default_queue_name
task_default_exchange = mx_default_queue_name
task_default_exchange_type = 'direct'
task_default_routing_key = mx_default_routing_key

# default exchange
default_exchange = Exchange(mx_default_queue_name, 'direct')

# topic exchange
topic_exchange = Exchange('mx_topic_exchange', 'topic')

# fanout 交换器设置
fanout_exchange = Exchange('new_arrival_fan_out', 'fanout')

# 任务队列设置
task_queues = (
    # Queue('fanout_queue_1', topic_exchange, routing_key='new_arrival.1.*'),
    # Queue('fanout_queue_2', topic_exchange, routing_key='new_arrival.*.2')
    Queue(mx_default_queue_name, exchange=default_exchange, routing_key=mx_default_routing_key),
    Queue('fanout_queue_1', exchange=fanout_exchange),
    Queue('fanout_queue_2', exchange=fanout_exchange),
)

# sync_sku_task_dummy
# task_routes = {
#     'sync_sku_task_dummy': {
#         'exchange': 'broadcast_tasks',
#     }
# }

# [周期作业]
beat_schedule = {
    'add-every-30-seconds': {
        'task': 'periodic_category_url_driver',
        'schedule': crontab(hour=4, minute=0)
    },
}


class MyRouter(object):
    # def route_for_task(self, task, args=None, kwargs=None):
    def route_for_task(self, task, args=None, kwargs=None):
        if task.startswith('sync_sku_task_dummy'):
            return {
                # fanout 交换器配置 exchange_type一定要设置否则失效
                "exchange": "new_arrival_fan_out",
                "exchange_type": "fanout",

                # 默认队列配置
                # 'queue': 'default_queue',
                # 'routing_key': 'default.route_key',
            }
        # 爬虫作业
        # good_detail_spider_task
        elif task.startswith('periodic_good_detail_spider_task.driver'):
            return {
                # 默认队列配置
                'queue': 'default_queue',
                'routing_key': 'default.route_key',
            }
        # 剩下的其实就会被放到默认队列
        else:
            return None


# CELERY_ROUTES本来也可以用一个大的含有多个字典的字典,但是不如直接对它做一个名称统配
task_routes = (MyRouter(),)
