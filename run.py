# Dont add anything which is not a app config
import os

from webApp import create_app

# To do load the config from the env like given below
# config_name = os.getenv('FLASK_CONFIG')

config_name = 'development'
app = create_app(config_name)


if __name__ == '__main__':
    app.run()