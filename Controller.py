# API 서버

from flask import Response, Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from functools import wraps

import json

import Database
import DataProcessor

db = Database.Database()
dp = DataProcessor.DataProcessor()


app = Flask(__name__)
CORS(app, resources={r'*': {'origins': 'http://localhost:3000'}})
api = Api(app)

def as_json(f): #한글 깨짐 방지 + json 데코레이터
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')
    return decorated_function

# KOSPI, KOSDAQ 지수 정보 가져오기 API
class Index(Resource):
    @as_json
    def get(self):
        df = db.최근1일지수데이터조회().to_json(orient='records', force_ascii=False, date_format='iso')
        parsed = json.loads(df)
        return parsed

# 주식 종목 리스트 조회 API
class StockList(Resource):
    @as_json
    def get(self):
        return db.종목정보조회()

# 분석 가능 종목 조회 API
class AvailableStockList(Resource):
    @as_json
    def get(self):
        df = db.분석가능종목조회().to_json(orient='records', force_ascii=False, date_format='iso')
        parsed = json.loads(df)
        return parsed

# 종목 코드로 종목명 가져오기 API
class StockName(Resource):
    def get(self, stockcode):
        return db.종목명조회(stockcode)

# 일봉데이터 조회 API
class StockDailyCandle(Resource):
    @as_json
    def get(self, stockcode, dates):
        df = dp.기간범위내일봉데이터(stockcode, int(dates)).to_json(orient='records', force_ascii=False, date_format='iso')
        parsed = json.loads(df)
        return parsed

# 특정 주식 N 거래일 간 고가 기울기, 저가 기울기 조회 API
class TriangularConvergence(Resource):
    @as_json
    def get(self, stockcode, dates):
        최고가시작점, 최고가끝점 = dp.기간범위내고가기울기(stockcode, int(dates))
        최저가시작점, 최저가끝점 = dp.기간범위내저가기울기(stockcode, int(dates))
        result = {"topprice": [str(최고가시작점), str(최고가끝점)], "lowprice": [str(최저가시작점), str(최저가끝점)]}
        return result

api.add_resource(Index, '/index')
api.add_resource(StockList, '/stocklist')
api.add_resource(AvailableStockList, '/availablestocklist')
api.add_resource(StockName, '/stockname/<stockcode>')
api.add_resource(StockDailyCandle, '/stockdailycandle/<stockcode>/<dates>')
api.add_resource(TriangularConvergence, '/stockdailycandle/triangularconvergence/<stockcode>/<dates>')

if __name__ == '__main__':
    app.run(debug=True)