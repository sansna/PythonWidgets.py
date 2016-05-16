from bottle import route, run, template
@route('/<first>/<name>')
def index(name,first):
    return template('<b>/Hello {{first}}{{name}}</b>',first=first,name=name)
run(host='192.168.24.134',port=8080)
