# 저장된 데이터를 필요에 맞게 가공하는 모듈

import Database
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

class DataProcessor:

    데이터베이스 = None

    def __init__(self):
        self.데이터베이스 = Database.Database()

    ## 데이터 연산용 함수들
    def 기간범위내일봉데이터(self, 종목코드, 일수):
        일봉데이터 = self.데이터베이스.종목일봉데이터조회(종목코드)
        일봉데이터['일자'] = pd.to_datetime(일봉데이터['일자'])
        일봉데이터.sort_values(by=['일자'], inplace=True, ascending=False)
        return 일봉데이터.head(일수)

    def 널값정리된신용데이터(self, 종목코드, 일수):
        신용데이터 = self.데이터베이스.종목신용데이터조회(종목코드)
        신용데이터 = 신용데이터.fillna(0)
        return 신용데이터.head(일수)

    def 기간범위내고가기울기(self, 종목코드, 일수):
        일봉데이터 = self.기간범위내일봉데이터(종목코드, 일수)
        일봉데이터 = 일봉데이터.iloc[:,[2]].values

        x = pd.DataFrame(np.arange(일수), columns=["번호"])
        x = x.iloc[:,[0]].head(일수).values

        데이터모델 = LinearRegression()
        데이터모델.fit(X = x, y = 일봉데이터) ## x, y에 대한 데이터 모델 생성

        return round((데이터모델.predict([[일수 - 1]])[0][0]), 2), round((데이터모델.predict([[0]])[0][0]), 2) #출력

    def 기간범위내저가기울기(self, 종목코드, 일수):
        일봉데이터 = self.기간범위내일봉데이터(종목코드, 일수)
        일봉데이터 = 일봉데이터.iloc[:,[3]].values
        x = pd.DataFrame(np.arange(일수), columns=["번호"])
        x = x.iloc[:,[0]].head(일수).values

        데이터모델 = LinearRegression()
        데이터모델.fit(X = x, y = 일봉데이터) ## x, y에 대한 데이터 모델 생성

        return round((데이터모델.predict([[일수 - 1]])[0][0]), 2), round((데이터모델.predict([[0]])[0][0]), 2) #출력


