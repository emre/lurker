# -*- coding: utf-8 -*-


def configuration_class_to_dict(related_class):
    """
    fetchs public properties of an object and returns it as dictionary.
    """
    dictionary = {}

    # blacklist
    lurker_options = [
        'ping_at_every_query',
        'cache_information',
        'cache',
        'autocommit',
        'supress_warnings',
    ]

    # __dict__ not used since it doesn't provide parent class's members.
    for key in dir(related_class):
        if not key.startswith('_') and key not in lurker_options:
            dictionary.update({key: getattr(related_class, key)})
    return dictionary
