import Collector
import Database

# 객체 선언
db = Database.Database() # mysql DB 연결 및 sql 작업용 객체
collector = Collector.Collector() # 키움 open api 사용 객체

collector.로그인()

# stock_code 테이블 업데이트
collector.종목사전생성()
db.종목정보저장(**collector.종목딕셔너리)

db.종목정보조회()
db.disconnect()
