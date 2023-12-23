from bs4 import BeautifulSoup
import urllib.request as req

def extract_seoul_weather(soup, user_date):
    for location in soup.find_all('location'):
        if location.city.get_text() == "서울":
            for data in location.find_all('data'):
                date = data.tmef.get_text()
                if user_date in date:
                    weather = data.wf.get_text()
                    min_temp = data.tmn.get_text()
                    max_temp = data.tmx.get_text()
                    rain_prob = data.rnst.get_text() if data.rnst else '없음'

                    return {
                        'date': date,
                        'weather': weather,
                        'min_temp': min_temp,
                        'max_temp': max_temp,
                        'rain_prob': rain_prob
                    }
    return None

# 기상청 중기예보 RSS 주소
url = "http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=109"


res = req.urlopen(url)
soup = BeautifulSoup(res, "html.parser")

# 사용자에게 날짜 입력 받기
user_date = input("조회하고 싶은 날짜를 입력하세요 (예: 2023-12-26): ")

# 서울 날씨 정보 출력
weather_info = extract_seoul_weather(soup, user_date)
if weather_info:
    print(f"{user_date}의 날씨 정보입니다.\n")
    print(f"예상 날씨: {weather_info['weather']}\n최저 기온: {weather_info['min_temp']}°C\n최고 기온: {weather_info['max_temp']}°C\n강수 확률: {weather_info['rain_prob']}%")
else:
    print(f"{user_date}에 대한 날씨 정보가 없습니다.")
