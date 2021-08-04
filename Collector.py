from pykiwoom.kiwoom import *
import datetime

class Collector:

    ####### 변수 #######
    kiwoom = None
    종목딕셔너리 = None

    ####### 함수 #######
    def __init__(self):
        self.kiwoom = Kiwoom()
        self.종목딕셔너리 = {}

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

        print(self.종목딕셔너리)

    def 최근1달일봉가져오기(self, 종목명):
        오늘날짜 = datetime.datetime.now()
        오늘날짜 = 오늘날짜.strftime("%Y%m%d")

        데이터 = self.kiwoom.block_request("opt10081",
                                   종목코드=self.종목딕셔너리[종목명],
                                   기준일자=오늘날짜,
                                   수정주가구분=1,
                                   output="주식일봉차트조회",
                                   next=0)
        #데이터.to_excel("실험.xlsx")



