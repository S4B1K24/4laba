from flask import Flask, Blueprint
from flask_restplus import Api, Resource
app = Flask(__name__)
api = Api(app = app)
name_space = api.namespace('main', description='Main APIs')
@name_space.route("/")
class MainClass(Resource):
    def get(self):
        return {"status": "Got new data"}
    def post(self):
        return {"status": "Posted new data"}

from flask_restplus import fields
list_ = api.model('list', {
    'id': fields.Integer(required=True, description='id film'),
    'author': fields.String(required=True, description='author film'),
    'name': fields.String(required=True, description='name film'),
    'time': fields.Float(required=True, description='time film'),
    'score': fields.Float(required=True, description='score film'),
    'array': fields.List(fields.Raw,required=True, description='all list')
})

ls=[{"id": 0, "author":"K.Tarantino", "name":"kill bill 1", "time":112, "score": 9.8}]
universalID=int(0)
allarray = ls
name_space1 = api.namespace('list', description='list APIs')
@name_space1.route("/")
class ListClass(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(list_)
    def get(self):
        """"Получение всего хранимого массива"""
        return { 'array': ls}
    @name_space1.doc("")
    @name_space1.expect(list_)
    @name_space1.marshal_with(list_)
    def post(self):
        """Создание массива/наше описание функции пост"""
        global allarray
        
        film={"id":api.payload['id'], "author": api.payload['author'], "name": api.payload['name'], "time": api.payload['time'], "score": api.payload['score'] } 

        ls.append(film)
        return { 'array': ls}
sortsc = api.model('lst', { 'array':fields.List(fields.Raw,required=True, description='all list')})
@name_space1.route("/getsortScore")
class getsortScore(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по оценке"""
        global ls
        sor=sorted(ls,key=lambda film: film['score'])
        return {'array': sor}

@name_space1.route("/getsorttime")
class getsortTime(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по времени"""
        global ls
        tim=sorted(ls,key=lambda film: film['time'])
        return {'array': tim}

@name_space1.route("/getsortauthor")
class getsortAuthor(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по автору"""
        global ls
        aut=sorted(ls,key=lambda film: film['author'])
        return {'array': aut}

@name_space1.route("/getsortname")
class getsortName(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по названию"""
        global ls
        nam=sorted(ls,key=lambda film: film['name'])
        return {'array': nam}

@name_space1.route("/getsortid")
class getsortId(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(sortsc)
    def get(self):
        """Получение сортировки по id"""
        global ls
        ide=sorted(ls,key=lambda film: film['id'])
        return {'array': ide}
oneval=api.model('one', {'val':fields.String}, required=True, description='one values')

@name_space1.route("/getmaxscore")
class getmaxscore(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение максимального по очкам"""
        global ls
        mx=max([film['score'] for film in ls ])
        return {'val': mx}

@name_space1.route("/getmaxtime")
class getmaxtime(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение максимального по времени"""
        global ls
        mx=max([film['time'] for film in ls ])
        return {'val': mx}

@name_space1.route("/getminscore")
class getminscore(Resource):
    @name_space1.doc("")
    # маршаллинг данных в соответствии с моделью minmax
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение минимального по оценке"""
        global ls
        mn=min([film['score'] for film in ls ])
        return {'val': mn}

@name_space1.route("/getmintime")
class getmintime(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение минимального по времени"""
        global ls
        mn=min([film['time'] for film in ls ])
        return {'val': mn}

@name_space1.route("/getsredscore")
class getsredscore(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение среднего по оценке"""
        global ls
        srd=sum([film['score'] for film in ls ])/len(ls)
        return {'val': srd}

@name_space1.route("/getsredtime")
class getsredtime(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение среднего по времени"""
        global ls
        srd=sum([film['time'] for film in ls ])/len(ls)
        return {'val': srd}

@name_space1.route("/getsredtime")
class getsortScore(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(oneval)
    def get(self):
        """Получение сортировки по id"""
        global ls
        srd=sum([film['time'] for film in ls ])/len(ls)
        return {'val': srd}

api.add_namespace(name_space1)

from flask_restplus import reqparse
from random import random

reqp = reqparse.RequestParser()
reqp.add_argument('id', type=int, required=False)

@name_space1.route("/izmdfilm")
class IzmfilClass(Resource):
    @name_space1.doc("")
    @name_space1.expect(reqp)
    @name_space1.marshal_with(list_)
    def get(self):
        """удаление фильма по ID"""
        global ls
        args = reqp.parse_args()
        ls=[film for film in ls if film['id']!=args['id']]
        return { 'array': ls}
    @name_space1.doc("")
    @name_space1.expect(list_)
    @name_space1.marshal_with(list_)
    def post(self):
        """Изменение фильма по id"""
        global ls
        for film in ls:
          if(api.payload['id'] == film["id"]):
                film["author"] = api.payload['author']
                film["name"] = api.payload['name']
                film["time"] = api.payload['time']
                film["score"] = api.payload['score']
                return { 'array': ls}
        
        film={"id":api.payload['id'], "author": api.payload['author'], "name": api.payload['name'], "time": api.payload['time'], "score": api.payload['score'] } 
        ls.append(film)
        return ls
app.run(debug=True)
