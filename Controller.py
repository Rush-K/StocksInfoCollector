# API 서버

from flask import Response, Flask
from flask_restful import Resource, Api
from functools import wraps

import json

import Database
import Collector

db = Database.Database()

collector = Collector.Collector()
collector.종목딕셔너리 = db.종목정보조회()

app = Flask(__name__)
api = Api(app)

def as_json(f): #한글 깨짐 방지 + json 데코레이터
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')
    return decorated_function

class StockList(Resource):
    @as_json
    def get(self):
        return db.종목정보조회()

class StockDailyCandle(Resource):
    def post(self, stockname):
        collector.로그인()
        데이터 = collector.최근1달일봉가져오기(stockname)
        return 데이터

api.add_resource(StockList, '/stocklist')
api.add_resource(StockDailyCandle, '/stockdailycandle/<stockname>')

if __name__ == '__main__':
    app.run(debug=True)