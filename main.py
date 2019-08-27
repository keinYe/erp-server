# -*- coding:utf-8 -*-

from pycrawler import create_app

app = create_app()

if __name__ == '__main__':
    # app = create_app()
    app.run(debug=True)
