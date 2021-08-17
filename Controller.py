# API 서버

from flask import Response, Flask
from flask_restful import Resource, Api
from functools import wraps

import json

import Database
import DataProcessor

db = Database.Database()
dp = DataProcessor.DataProcessor()


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
    def get(self, stockcode):
        return db.종목일봉데이터조회(stockcode).to_json(force_ascii=False)

class StockLowPriceGraph(Resource):
    def get(self, stockcode, dates):
        return dp.기간범위내최저가기울기(stockcode, int(dates))

api.add_resource(StockList, '/stocklist')
api.add_resource(StockDailyCandle, '/stockdailycandle/<stockcode>')
api.add_resource(StockLowPriceGraph, '/stockdailycandle/<stockcode>/<dates>')

if __name__ == '__main__':
    app.run(debug=True)