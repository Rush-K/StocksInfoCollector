# Mysql 데이터베이스

import MySQLdb
import pandas
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

    def 종목데이터저장(self, 종목코드, 데이터):
        print("daily_{} 테이블 처리중..".format(종목코드))

        try:
            sql = "select * from daily_{}".format(종목코드)
            self.cursor.execute(sql)
            기존데이터 = DataFrame(self.cursor)
            데이터기준 = 기존데이터[0].max() < 데이터['일자']
            데이터 = 데이터[데이터기준]
            if 데이터.empty:
                print("추가할 데이터가 없습니다.")
            else:
                print("새로운 데이터 발견, 추가중..")
                데이터.to_sql('daily_{}'.format(종목코드), self.engine, if_exists='append', index=False)
            print("daily_{} 테이블 업데이트 완료".format(종목코드))
        except MySQLdb.ProgrammingError as e:
            데이터.to_sql('daily_{}'.format(종목코드), self.engine, if_exists='append', index=False)
            sql = "alter table daily_{} add primary key(일자)".format(종목코드)
            self.cursor.execute(sql)
            print("daily_{} 신규 테이블 생성 후 저장 완료".format(종목코드))

    def 지수데이터저장(self, 데이터):
        print("daily_index 테이블 처리중..")

        try:
            sql = "select * from daily_index"
            self.cursor.execute(sql)
            기존데이터 = DataFrame(self.cursor)
            데이터기준 = 기존데이터[0].max() < 데이터['일자']
            데이터 = 데이터[데이터기준]
            if 데이터.empty:
                print("추가할 데이터가 없습니다.")
            else:
                print("새로운 데이터 발견, 추가중..")
                데이터.to_sql('daily_index', self.engine, if_exists='append', index=False)
            print("daily_index 테이블 업데이트 완료")
        except MySQLdb.ProgrammingError as e:
            데이터.to_sql('daily_index', self.engine, if_exists='append', index=False)
            sql = "alter table daily_index add primary key(일자)"
            self.cursor.execute(sql)
            print("daily_index 신규 테이블 생성 후 저장 완료")

    ## 데이터 조회 ##
    def 종목정보조회(self):
        sql = "select * from stock_code"
        self.cursor.execute(sql)

        result = {}

        for row in self.cursor:
            result[row[0]] = row[1]

        return result

    def 분석가능종목조회(self):
        sql = "select table_name from information_schema.tables where table_schema='stock'"
        self.cursor.execute(sql)
        테이블목록 = DataFrame(self.cursor)
        테이블목록 = 테이블목록[테이블목록[0].str.contains("daily_")]
        테이블목록 = 테이블목록[테이블목록[0] != "daily_index"]
        테이블목록.columns = ['종목코드']
        테이블목록['종목코드'] = 테이블목록['종목코드'].str.replace('daily_', '')

        result = DataFrame()

        for 종목코드 in 테이블목록['종목코드']:
            sql = "select s_name from stock_code where s_code='{}'".format(종목코드)
            self.cursor.execute(sql)
            result = pandas.concat([result, DataFrame({'종목명': [DataFrame(self.cursor).iloc[0, 0]], '종목코드': [종목코드]})], ignore_index=True)

        return result


    def 종목일봉데이터조회(self, 종목코드):
        sql = "select 일자, 현재가, 고가, 저가, 거래량 from daily_{}".format(종목코드)
        self.cursor.execute(sql)

        result = DataFrame(self.cursor)
        result.columns = ["일자", "현재가", "고가", "저가", "거래량"]
        return result

    def 종목신용데이터조회(self, 종목코드):
        sql = "select 일자, 융자잔고, 대주잔고 from daily_{}".format(종목코드)
        self.cursor.execute(sql)

        result = DataFrame(self.cursor)
        result.columns = ["일자", "융자잔고", "대주잔고"]
        return result