# -*- coding: utf-8 -*-

from lurker_exceptions import LurkerInvalidConfigurationObjectException

class Connection(object):

    def __init__(self, Configuration):
        if not hasattr(Configuration, 'configuration_object_check'):
            raise LurkerInvalidConfigurationObjectException('First parameter of the Connection object must be a '\
                                                            'BaseConfig instance.')
