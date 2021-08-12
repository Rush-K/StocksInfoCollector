# 필요한 데이터를 Collector 모듈을 통해서 가져오고, Database에 저장하는 파일

import Collector
import Database

# 객체 선언
db = Database.Database() # mysql DB 연결 및 sql 작업용 객체
collector = Collector.Collector() # 키움 open api 사용 객체

# 일봉데이터 받을 종목 리스트
stockList = ['삼성전자', '두산중공업', '기아']

collector.로그인()

# stock_code 테이블 업데이트
collector.종목사전생성()
db.종목정보저장(**collector.종목딕셔너리)

# 종목별 일봉데이터 DB 저장
for 종목명 in stockList:
    db.일봉데이터저장(collector.종목딕셔너리[종목명], collector.최근1달일봉가져오기(종목명))

