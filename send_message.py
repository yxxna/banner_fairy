from dotenv import load_dotenv
import os
import datetime
from slack_sdk import WebClient



# ✅ 슬랙 채널 ID 설정
# channel_id = "C08KRL1B4EB"
# 테스트용 채널로 보내고 싶으면 아래 줄 주석 해제
channel_id = "C08L22G50CA"

# ✅ 환경 변수 불러오기
load_dotenv()
slack_token = os.getenv("SLACK_TOKEN")
client = WebClient(token=slack_token)



# 👇 공휴일 리스트 (2025년 예시)
KOREAN_HOLIDAYS = [
    "2025-01-01", "2025-03-01", "2025-05-05", "2025-06-06", "2025-08-15",
    "2025-10-03", "2025-12-25"
]

scheduled_days = [5, 10, 15]
today = datetime.date.today()

# ✅ 날짜가 주말 or 공휴일인지?
def is_holiday_or_weekend(date):
    return date.weekday() >= 5 or date.strftime("%Y-%m-%d") in KOREAN_HOLIDAYS

def get_next_working_day(date):
    # 👉 기준일 다음 날부터 확인
    date += datetime.timedelta(days=1)
    while is_holiday_or_weekend(date):
        date += datetime.timedelta(days=1)
    return date

# ✅ 오늘이 메시지 보내는 날인지 확인
def should_send_message():
    for day in scheduled_days:
        try:
            base_date = today.replace(day=day)
        except ValueError:
            continue  # 2월 30일 같은 날짜 예외 처리
        send_day = get_next_working_day(base_date) if is_holiday_or_weekend(base_date) else base_date
        if send_day == today:
            return day
    return None

# ✅ 담당자 멘션 자동 매칭
def get_mention(day):
    if day == 5:
        return "<@U02BG5HQZV4>"  # 권씨 슬랙 ID
    elif day == 10:
        return "<@U05B537RSJC>"  # 김씨 슬랙 ID
    elif day == 15:
        return "<@U050BP0GUNA>"  # 문씨 슬랙 ID
    return ""

# ✅ 날짜별 텍스트 자동 매칭
def get_text(day, mention):
    if day == 5:
        return f'''🗓️ {day}일 인증완료 배너 제작 요청일입니다! 아래 텍스트를 채워 해당 채널에 보내주세요! 강유나 멘션은 필수입니다! ❤️

1. 배너 목적 – 이 배너에서 강조하고자 하는 것이 무엇인가요? 최종 목적은 무엇인가요? (낮은 이자 대출 홍보, 보험 가입, 카드 발급 등)
2. 타겟 사용자 – 이 배너는 어떤 사용자에게 노출되나요? 어떤 사람들에게 노출되는 건가요? (예: 대출 심사를 받은 50대 등)
3. 메인 문구 – 가장 강조해야 하는 문장을 써주세요. 키워드로 작성해도 좋아요
4. 보조 문구 – 보조적으로 쓰이는 문장은? 쓰셨던 텍스트 요약해서 작성해줘도 좋아요
5. CTA (있다면) – 어떤 행동을 하길 원하는가요?
6. 디자인 참고자료 – 디자인에서 피해갈 요소가 있나요? (예: 특정 색상, 문구 등)
7. 희망 색상/톤:

👤 담당자: {mention}
'''
    elif day == 10:
        return f'''🗓️ {day}일 앱 푸시 배너 제작 요청일입니다! 아래 텍스트를 채워 해당 채널에 보내주세요! 강유나 멘션은 필수입니다! ❤️

1. 배너 목적 – 이 배너에서 강조하고자 하는 것이 무엇인가요? 최종 목적은 무엇인가요? (낮은 이자 대출 홍보, 보험 가입, 카드 발급 등)
2. 타겟 사용자 – 이 배너는 어떤 사용자에게 노출되나요? 어떤 사람들에게 노출되는 건가요? (예: 대출 심사를 받은 50대 등)
3. 메인 문구 – 가장 강조해야 하는 문장을 써주세요. 키워드로 작성해도 좋아요
4. 보조 문구 – 보조적으로 쓰이는 문장은? 쓰셨던 텍스트 요약해서 작성해줘도 좋아요
5. CTA (있다면) – 어떤 행동을 하길 원하는가요?
6. 디자인 참고자료 – 디자인에서 피해갈 요소가 있나요? (예: 특정 색상, 문구 등)
7. 희망 색상/톤:

👤 담당자: {mention}
'''
    elif day == 15:
        return f'''🗓️ {day}일 대출비교 프로모션 배너 제작 요청일입니다! 아래 텍스트를 채워 해당 채널에 보내주세요! 강유나 멘션은 필수입니다! ❤️

1. 배너 목적 – 이 배너에서 강조하고자 하는 것이 무엇인가요? 최종 목적은 무엇인가요? (낮은 이자 대출 홍보, 보험 가입, 카드 발급 등)
2. 타겟 사용자 – 이 배너는 어떤 사용자에게 노출되나요? 어떤 사람들에게 노출되는 건가요? (예: 대출 심사를 받은 50대 등)
3. 메인 문구 – 가장 강조해야 하는 문장을 써주세요. 키워드로 작성해도 좋아요
4. 보조 문구 – 보조적으로 쓰이는 문장은? 쓰셨던 텍스트 요약해서 작성해줘도 좋아요
5. CTA (있다면) – 어떤 행동을 하길 원하는가요?
6. 디자인 참고자료 – 디자인에서 피해갈 요소가 있나요? (예: 특정 색상, 문구 등)
7. 희망 색상/톤:

👤 담당자: {mention}
'''
    return None

# ✅ 메시지 보내기
send_day = should_send_message()
# 테스트 '배너요정 테스트 채널'로 보내고 싶으면 아래 코드 한 줄 주석 풀기 
# send_day = 5
if send_day:
    mention = get_mention(send_day)
    text = get_text(send_day, mention)
    if text:
        response = client.chat_postMessage(channel=channel_id, text=text)
        print("✅ 메시지 전송 완료:", response)


#import schedule
#import time


# 매일 아침 9시에 실행
schedule.every().day.at("10:30").do(run_bot)

print("⏰ 슬랙 메시지 봇이 실행 중입니다...")






