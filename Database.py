import MySQLdb

class Database:

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

        self.connect.commit()
        print("종목 딕셔너리 DB 저장 완료, 총 " + str(total) + "종목 중 " + str(update) + "개 추가 완료")


    ## 데이터 조회 ##
    def 종목정보조회(self):
        sql = "select * from stock_code"
        self.cursor.execute(sql)

        result = self.cursor.fetchall()
        print(result)

    def 일봉데이터전체조회(self):
        sql = "select * from daily_candle"
        self.cursor.execute(sql)

        result = self.cursor.fetchall()
        print(result)


    def disconnect(self):
        self.connect.close()


