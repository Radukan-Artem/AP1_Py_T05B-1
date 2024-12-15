from web.route.app_creator import *

if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port=5000)