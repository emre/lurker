# -*- coding: utf-8 -*-

def class_to_dict(related_class):
    """
    fetchs public properties of an object and returns it as dictionary.
    """
    dictionary = {}

    # __dict__ not used since it doesn't provide parent class's members.
    for key in dir(related_class):
        if not key.startswith('_'):
            dictionary.update({key: getattr(related_class, key)})
    return dictionary
