# -*- coding: utf-8 -*-
import os
from wownder import create_app

if __name__ == "__main__":
    _local_dir = os.path.dirname(os.path.abspath(__file__))
    app = create_app()
    # app.run(port=5080)
    context = (os.path.join(_local_dir, 'cert/server.crt'),
               os.path.join(_local_dir, 'cert/server.key'))
    app.run(host='0.0.0.0', port=5000, ssl_context=context, threaded=False,
            extra_files=[os.path.join(app.root_path, app.template_folder, 'layout.html')])
