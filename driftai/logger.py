import logging

from driftai.utils import SingletonDecorator

@SingletonDecorator
class DriftAILogger(object):
    def __init__(self):
        logging.basicConfig(format='[%(levelname)s] %(name)s - %(message)s')
        self.logger = logging.getLogger('DriftAI Logger')
        self.level = logging.DEBUG
    
    @property
    def level(self):
        return self.logger.getEffectiveLevel()

    @level.setter
    def level(self, level):
        self.logger.setLevel(level)

    def __getattr__(self, attr):
        return getattr(self.logger, attr)