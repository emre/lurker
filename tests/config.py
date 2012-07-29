import sys

sys.path.append('..')

from lurker.configuration import BaseLurkerConfig
from lurker.cache.backends.redis_backend import RedisBackend

class TestConfig(BaseLurkerConfig):
    """
    required table and sample data for tests:
    CREATE TABLE IF NOT EXISTS `people` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(255) NOT NULL,
         PRIMARY KEY (`id`)
    ) ENGINE=InnoDB  AUTO_INCREMENT=5 ;


    INSERT INTO `people` (`id`, `name`) VALUES
    (1, 'John Doe'),
    (2, 'Muhittin Hoca'),
    (4, 'Foo Bar');
    """
    host = 'localhost'
    user = 'root'
    passwd = 'yemre'
    db = 'lurker'
    cache = True
    cache_information = {
        'backend': RedisBackend,
        'args': (),
        'kwargs': {'host': 'localhost', 'port': 6379, 'db': 0},
        }


class FakeConfig(object):
    pass


