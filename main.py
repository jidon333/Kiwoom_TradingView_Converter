import pandas as pd
import sys

# 각 거래소 별 티커 목록을 딕셔너리로 저장
def load_tickers(fileName):
    with open(fileName, 'r') as file:
        # 파일의 첫 번째 줄을 읽고, 콤마로 구분하여 리스트로 변환
        tickers = file.readline().split(',')
        return tickers
    
def get_pure_ticker(exchange_ticker_name : str):
    ticker_str = exchange_ticker_name
    ticker_str = ticker_str.replace("NASDAQ:", "")
    ticker_str = ticker_str.replace("NYSE:", "")
    ticker_str = ticker_str.replace("AMEX:", "")
    return ticker_str



def tv_to_kiwoom():
    print('트레이딩뷰 .txt 파일을 키움 csv 파일 포멧으로 변경')
    fileName = input("트레이딩뷰 내보내기 .txt 파일의 이름을 입력하세요. ex) MyWatchList.txt \n")
    try:
        tickers = load_tickers(fileName)
    except Exception as e:
        print(e)
        print('파일명을 확인하세요')
        exit()
    print(tickers)

    pure_tickers = []
    for i, ticker in enumerate(tickers):
        pure_ticker = get_pure_ticker(ticker)
        pure_tickers.append(pure_ticker)

    print(pure_tickers)
    with open('kiwoom_format.csv', 'w', encoding='utf-8-sig') as file:
        for item in pure_tickers:
            file.write(f"{item},\n")

    print("파일 저장 완료. kiwoom_format.csv를 확인하세요")
    

def kiwoom_to_tv():
    print('키움 csv 포멧을 트레이딩뷰 .txt 파일로 변환')
    fileName = input("키움증권 내보내기 파일의 이름을 입력하세요. ex) input.csv \n")
    try:
        data = pd.read_csv(fileName, encoding='euc-kr', header=1, skip_blank_lines=True)
    except Exception as e:
        print(e)
        print('파일명을 확인하세요')
        exit()

    try:
        # '종목코드' 열이 있는지 시도
        tickers = data['종목코드']
    except KeyError:
        # '종목코드' 열이 없으면 'Symbol' 열을 사용
        tickers = data['Symbol']

    tickers = tickers.dropna()
    tickers = tickers.tolist()

    # 거래소 명칭 변경
    new_tickers = []
    for ticker in tickers:
        if "'ND" in ticker:
            new_ticker = str(ticker).replace("'ND", "'NASDAQ:")
        elif "'NY" in ticker:
            new_ticker = str(ticker).replace("'NY", "'NYSE:")
        elif "'NA" in ticker:
            new_ticker = str(ticker).replace("'NA", "'AMEX:")
        else:
            new_ticker = ticker
        new_tickers.append(new_ticker)
            
        
    # 리스트 l의 각 요소에서 ' 문자 제거
    new_tickers = [item.replace("'", "") for item in new_tickers]

    # 결과 확인
    print(new_tickers)

    # 거래소 별 티커 목록 불러오기
    tickers_amex = load_tickers('AMEX.txt')

    # 리스트의 티커들을 확인하고 거래소 정보 업데이트
    for i, ticker in enumerate(new_tickers):
        only_ticker = get_pure_ticker(ticker)
        if only_ticker in tickers_amex:
            new_tickers[i] = f'AMEX:{only_ticker}'



    # 리스트 l의 내용을 'output.txt' 파일로 저장
    with open('tradingView_format.txt', 'w') as file:
        for item in new_tickers:
            file.write(f"{item},")

    print("파일 저장 완료. tradingView_format.txt를 확인하세요. ")

################# main #################


while True:
    input_res = input(" 1: Kiwoom to Tranding View \n 2: Tranding view to Kiwoom \n 3: exit \n ")
    if input_res == '1':
        kiwoom_to_tv()
        sys.exit()
    elif input_res == '2':
        tv_to_kiwoom()
        sys.exit()
    elif input_res == '3':
        sys.exit()
    else:
        print("input error!")
    

