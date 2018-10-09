# -*- coding: utf-8 -*-
# author: bao

from model_message import create_app

app = create_app()


if __name__ == '__main__':
    app.run("0.0.0.0", port=9724, threaded=True)