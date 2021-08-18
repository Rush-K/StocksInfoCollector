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

# 주식 종목 리스트 조회 API
class StockList(Resource):
    @as_json
    def get(self):
        return db.종목정보조회()

# 일봉데이터 조회 API
class StockDailyCandle(Resource):
    @as_json
    def get(self, stockcode):
        df = db.종목일봉데이터조회(stockcode).to_json(orient='index', force_ascii=False, date_format='iso')
        parsed = json.loads(df)
        return parsed

# 특정 주식 N 거래일 간 고가 기울기, 저가 기울기 조회 API
class TriangularConvergence(Resource):
    @as_json
    def get(self, stockcode, dates):
        result = {'topprice': dp.기간범위내고가기울기(stockcode, int(dates)), 'lowprice': dp.기간범위내저가기울기(stockcode, int(dates))}
        return result

api.add_resource(StockList, '/stocklist')
api.add_resource(StockDailyCandle, '/stockdailycandle/<stockcode>')
api.add_resource(TriangularConvergence, '/stockdailycandle/triangularconvergence/<stockcode>/<dates>')

if __name__ == '__main__':
    app.run(debug=True)