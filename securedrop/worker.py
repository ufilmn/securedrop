import os

from flask import current_app
from redis import Redis
from rq import Queue


class RqWorkerQueue(object):

    '''
    A reference to a `rq` worker queue.

    Configuration:
        `RQ_WORKER_NAME`: Name of the `rq` worker.
    '''

    __EXT_NAME = 'rq-worker-queue'

    def __init__(self, app=None):
        self.__app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.__app = app
        self.__app.config.setdefault('RQ_WORKER_NAME', 'default')

        if not hasattr(self.__app, 'extensions'):
            self.__app.extensions = {}

        queue_name = self.__app.config['RQ_WORKER_NAME']
        queue = Queue(name=queue_name, connection=Redis(), default_timeout=3600)
        self.__app.extensions[self.__EXT_NAME] = queue

    def enqueue(self, *nargs, **kwargs):
        return (self.__app or current_app).extensions[self.__EXT_NAME].enqueue(*nargs, **kwargs)


rq_worker_queue = RqWorkerQueue()
