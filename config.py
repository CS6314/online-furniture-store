class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
    SECRET_KEY ='ZVWS36GD4o'

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    MYSQL_DATABASE_PASSWORD = 'akash123'
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_DB = 'flask_todo_list'
    MYSQL_DATABASE_HOST = 'localhost'
    MYSQL_DATABASE_PORT = 3306


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
