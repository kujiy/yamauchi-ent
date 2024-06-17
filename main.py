import time
from datetime import datetime, timezone, timedelta

from gtts import gTTS
from playsound import playsound

JST = timezone(timedelta(hours=+9))

def zenkaku_to_hankaku(text):
    # 全角数字を半角数字に変換する
    translation_table = str.maketrans('０１２３４５６７８９', '0123456789')
    return text.translate(translation_table)

def speak_text(text, lang='ja'):
    # gTTSオブジェクトの作成
    tts = gTTS(text=text, lang=lang)

    # 音声ファイルとして保存
    tts.save("output.mp3")

    # 音声ファイルを再生
    playsound("output.mp3")


# 例


import requests
from bs4 import BeautifulSoup

def main():
    # URLの取得
    url = 'https://ssc6.doctorqube.com/yamauchi-jibika/'
    response = requests.get(url)

    # HTMLのパース
    soup = BeautifulSoup(response.content, 'html.parser')

    # 特定のspanタグの内容を取得
    waitlist_span = soup.find('span', class_='waitlistall')
    if waitlist_span:
        waitlist_numbers = waitlist_span.get_text()
        waitlist_numbers_hankaku = zenkaku_to_hankaku(waitlist_numbers)
        waitlist_numbers_list = [int(num) for num in waitlist_numbers_hankaku.split('、')]

        print(f"お待ちの方の番号: {waitlist_numbers}")
        first = waitlist_numbers_list[0]
        if first > 40:
            speak_text(str("行こう行こう行こう行こう行こう行こう行こう"))
        # もし現在時刻が11:20amを超えていたら、行こうを出力
        else:
            # Get the current time in JST
            now = datetime.now(JST).time()
            # Define the desired time
            desired_time = datetime.strptime('11:20', '%H:%M').time()

            # Compare the current time with the desired time
            if now > desired_time:
                speak_text(str("時間切れだよ。行こう行こう行こう行こう行こう行こう行こう"))

        speak_text(str(first))

    else:
        print("指定されたspanタグが見つかりませんでした。")

for i in range(1000):
    main()
    time.sleep(5)