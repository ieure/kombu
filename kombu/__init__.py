"""AMQP Messaging Framework for Python"""
VERSION = (1, 0, 8)
__version__ = ".".join(map(str, VERSION[0:3])) + "".join(VERSION[3:])
__author__ = "Ask Solem"
__contact__ = "ask@celeryproject.org"
__homepage__ = "http://github.com/ask/kombu/"
__docformat__ = "restructuredtext en"

import os
import sys
if not os.environ.get("KOMBU_NO_EVAL", False):
    # Lazy loading.
    # - See werkzeug/__init__.py for the rationale behind this.
    from types import ModuleType

    all_by_module = {
            "kombu.connection": ["BrokerConnection"],
            "kombu.entity": ["Exchange", "Queue"],
            "kombu.messaging": ["Consumer", "Producer"],
    }

    object_origins = {}
    for module, items in all_by_module.iteritems():
        for item in items:
            object_origins[item] = module

    class module(ModuleType):

        def __getattr__(self, name):
            if name in object_origins:
                module = __import__(object_origins[name], None, None, [name])
                for extra_name in all_by_module[module.__name__]:
                    setattr(self, extra_name, getattr(module, extra_name))
                return getattr(module, name)
            return ModuleType.__getattribute__(self, name)

        def __dir__(self):
            result = list(new_module.__all__)
            result.extend(("__file__", "__path__", "__doc__", "__all__",
                           "__docformat__", "__name__", "__path__", "VERSION",
                           "__package__", "__version__", "__author__",
                           "__contact__", "__homepage__", "__docformat__"))
            return result

    # keep a reference to this module so that it's not garbage collected
    old_module = sys.modules[__name__]

    new_module = sys.modules[__name__] = module(__name__)
    new_module.__dict__.update({
        "__file__": __file__,
        "__path__": __path__,
        "__doc__": __doc__,
        "__all__": tuple(object_origins),
        "__version__": __version__,
        "__author__": __author__,
        "__contact__": __contact__,
        "__homepage__": __homepage__,
        "__docformat__": __docformat__,
        "VERSION": VERSION})

if os.environ.get("KOMBU_LOG_DEBUG"):
    os.environ.update(KOMBU_LOG_CHANNEL="1", KOMBU_LOG_CONNECTION="1")
    from kombu.utils import debug
    debug.setup_logging()
