# 키움 API 호출로 필요한 데이터를 가져오는 모듈

from pykiwoom.kiwoom import *
from pandas import DataFrame
import datetime

class Collector:

    ####### 변수 #######
    kiwoom = None
    종목딕셔너리 = None
    오늘날짜 = None

    ####### 함수 #######
    def __init__(self):
        self.kiwoom = Kiwoom()
        self.종목딕셔너리 = {}
        self.오늘날짜 = datetime.datetime.now()
        #self.오늘날짜 -= datetime.timedelta(days=1)
        self.오늘날짜 = self.오늘날짜.strftime("%Y%m%d")

    def 로그인(self):
        self.kiwoom.CommConnect(block=True)

        계좌정보 = self.kiwoom.GetLoginInfo("ACCNO")
        사용자ID = self.kiwoom.GetLoginInfo("USER_ID")
        사용자이름 = self.kiwoom.GetLoginInfo("USER_NAME")

        print(계좌정보)
        print(사용자ID + "(" + 사용자이름 + ") 님 접속")

    def 종목사전생성(self):
        # 코스피 종목 사전 추가
        코스피종목코드리스트 = self.kiwoom.GetCodeListByMarket('0')
        for i in 코스피종목코드리스트:
            self.종목딕셔너리[self.kiwoom.GetMasterCodeName(i)] = i

        # 코스닥 종목 사전 추가
        코스닥종목코드리스트 = self.kiwoom.GetCodeListByMarket('10')
        for i in 코스닥종목코드리스트:
            self.종목딕셔너리[self.kiwoom.GetMasterCodeName(i)] = i

        print("종목딕셔너리 생성 완료")

    def 지수가져오기(self):
        코스피 = self.kiwoom.block_request("opt20003",
                                   업종코드="001",
                                   output="KOSPI지수",
                                   next=0)

        코스닥 = self.kiwoom.block_request("opt20003",
                                        업종코드="101",
                                        output="KOSDAQ지수",
                                        next=0)

        코스피 = DataFrame(코스피.head(1), columns=['현재가', '전일대비'])
        코스피.columns = ['KOSPI현재가', 'KOSPI전일대비']
        코스닥 = DataFrame(코스닥.head(1), columns=['현재가', '전일대비'])
        코스닥.columns = ['KOSDAQ현재가', 'KOSDAQ전일대비']

        지수데이터 = pd.concat([코스피.head(1), 코스닥.head(1)], axis=1)
        지수데이터.insert(0, '일자', self.오늘날짜)
        지수데이터['일자'] = pd.to_datetime(지수데이터['일자'])

        return 지수데이터

    def 일봉가져오기(self, 종목명):
        데이터 = self.kiwoom.block_request("opt10081",
                                   종목코드=self.종목딕셔너리[종목명],
                                   기준일자=self.오늘날짜,
                                   수정주가구분=1,
                                   output="주식일봉차트조회",
                                   next=0)

        데이터 = DataFrame(데이터, columns=['일자', '현재가', '고가', '저가', '거래량'])
        데이터['일자'] = pd.to_datetime(데이터['일자'])
        데이터 = 데이터.astype({'현재가': 'int', '고가': 'int', '저가': 'int', '거래량': 'int'})

        return 데이터

    def 신용매매동향가져오기(self, 종목명):
        융자잔고데이터 = self.kiwoom.block_request("opt10013",
                                  종목코드=self.종목딕셔너리[종목명],
                                  일자=self.오늘날짜,
                                  조회구분="1", # 조회구분 1 : 융자, 2 : 대주(공매도)
                                  output="신용매매동향",
                                  next=0)

        잔고데이터 = DataFrame(융자잔고데이터, columns=['잔고'])
        잔고데이터.columns = ['융자잔고']

        대주잔고데이터 = self.kiwoom.block_request("opt10013",
                                  종목코드=self.종목딕셔너리[종목명],
                                  일자=self.오늘날짜,
                                  조회구분="2", # 조회구분 1 : 융자, 2 : 대주(공매도)
                                  output="신용매매동향",
                                  next=0)

        잔고데이터['대주잔고'] = DataFrame(대주잔고데이터, columns=['잔고'])

        return 잔고데이터

