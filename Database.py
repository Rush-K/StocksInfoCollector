# Mysql 데이터베이스

import MySQLdb
from pandas import DataFrame
from sqlalchemy import create_engine # dataframe 저장할 때만 사용 : MySQLdb 보다 속도가 느림

class Database:

    engine = None
    connect = None
    cursor = None

    def __init__(self):
        self.connect = MySQLdb.connect(
            user='root',
            passwd='root',
            host='localhost',
            db='stock',
            charset='utf8mb4')

        self.cursor = self.connect.cursor()
        self.engine = create_engine("mysql+mysqldb://root:" + "root" + "@localhost/stock?charset=utf8mb4", encoding='utf-8')

    ## 데이터 삽입 ##
    def 종목정보저장(self, **종목딕셔너리):
        update = 0
        total = len(종목딕셔너리)

        for 종목이름, 종목코드 in 종목딕셔너리.items():
            sql = "insert into stock_code(s_name, s_code) values('{}', '{}')".format(종목이름, 종목코드)
            try:
                self.cursor.execute(sql)
                update = update + 1
            except MySQLdb.IntegrityError as e:
                pass
            except MySQLdb.ProgrammingError as e:
                pass

        self.connect.commit()
        print("종목 딕셔너리 DB 저장 완료, 총 " + str(total) + "종목 중 " + str(update) + "개 추가 완료")

    def 일봉데이터저장(self, 종목코드, 데이터):
        데이터.to_sql('daily_candle_{}'.format(종목코드), self.engine, if_exists='replace', index=False)
        print(종목코드 + " 저장 완료")

    ## 데이터 조회 ##
    def 종목정보조회(self):
        sql = "select * from stock_code"
        self.cursor.execute(sql)

        result = {}

        for row in self.cursor:
            result[row[0]] = row[1]

        return result

    def 종목일봉데이터조회(self, 종목코드):
        sql = "select * from daily_candle_{}".format(종목코드)
        self.cursor.execute(sql)

        result = DataFrame(self.cursor)
        result.columns = ["일자", "현재가", "고가", "저가", "거래량"]
        return result