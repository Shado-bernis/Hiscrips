import os
import time

from flask import Flask, make_response, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)
@app.route('/')
def hello_word():
    posting=[]
    path_dir = 'files'
    file_list = os.listdir(path_dir)
    return render_template('index.html',f = file_list)
@app.route('/write',methods = {'GET', 'POST'})
def write():
    if request.method =='POST':
        title = request.form['title']
        descrtiption = request.form['description']

        if len(descrtiption) > 3:
            filename = time.strftime('%H%M%S')
            with open('files/%s.txt'%filename, 'w') as f:
                f.write('%s' %title)
                f.write('\n')
                f.write('%s'%descrtiption)

        path_dir = 'files'
        file_list = os.listdir(path_dir)

        posting = []

        for name in file_list:
            print(name)

            with open('files/%s.txt'%name[:-4],'r') as f:
                sw=True
                t=''
                c=''
                for line in f:
                    if sw:
                        t=line
                        sw=False
                    else:
                        c = c + line
                posting.append([t,c,name])
        print(posting)
    return render_template('index.html',p=posting)


@app.route('/delete/<id>', methods = ['DELETE'])
def delete(id):
    if request.method == 'DELETE':
        print(id)
        
        os.remove('files/%s' % id)
    return make_response(jsonify(
        {
            'status' : True
        }), 200
    )

if __name__ == '__main__':
    app.debug = True
    app.run(port='8080',debug=True)
