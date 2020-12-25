import easyocr 
import time
import bottle 
import json
import os
from bottle import request, response
from bottle import route, run
tic = time.perf_counter()
reader = easyocr.Reader(['en'])
toc = time.perf_counter()
print(f'Setup completed in {toc - tic:0.4f} seconds')
tic = time.perf_counter()
# for _ in range(50):
#     bounds = reader.readtext('/examples/screenshot.png', detail = 0)
toc = time.perf_counter()
print(f'OCR completed in {toc - tic:0.4f} seconds')
#print(bounds) 



app = application = bottle.default_app()


@route('/upload', method='POST')
def do_upload():
    category = request.forms.get('category')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return "File extension not allowed."

    save_path = "/examples/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path, overwrite=True)
    #return "File successfully saved to '{0}'.".format(save_path)
    bounds = reader.readtext(file_path, detail = 0)
    return json.dumps({'bounds': bounds})

@route('/')
def hello_world():
    response.headers['Content-Type'] = 'application/json'
    bounds = reader.readtext('/examples/screenshot.png', detail = 0)
    return json.dumps({'bounds': bounds})

if __name__ == '__main__':
    bottle.run(host = '0.0.0.0', port = 8000)