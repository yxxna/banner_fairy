# # ------------------------------------------ 2025.08.19 new 코드 
# send_message.py
from dotenv import load_dotenv
import os
import datetime as dt
from slack_sdk import WebClient

# -------------------------------
# 0) 기본 설정 & 클라이언트
# -------------------------------
load_dotenv()

SLACK_TOKEN = os.getenv("SLACK_TOKEN")  # GitHub Secrets에 저장돼 있어야 함
if not SLACK_TOKEN:
    raise RuntimeError("SLACK_TOKEN 이 설정되어 있지 않아요. GitHub Secrets에 SLACK_TOKEN을 추가해주세요.")


# ✅ 슬랙 채널 ID 설정 (채널명 : 배너요정) 
CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID", "C08KRL1B4EB")

# 테스트 채널 ID: 환경변수에 없으면 테스트 채널로 기본값
# CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID", "C08L22G50CA")

client = WebClient(token=SLACK_TOKEN)

# -------------------------------
# 1) 일정/공휴일
# -------------------------------
SCHEDULED_DAYS = (5, 10, 15)

KOREAN_HOLIDAYS = {
    "2025-01-01", "2025-03-01", "2025-05-05", "2025-06-06", "2025-08-15",
    "2025-10-03", "2025-12-25",
}

def is_holiday_or_weekend(d: dt.date) -> bool:
    """토/일 또는 공휴일이면 True"""
    return d.weekday() >= 5 or d.strftime("%Y-%m-%d") in KOREAN_HOLIDAYS

def push_to_next_working_day(d: dt.date) -> dt.date:
    """주말/공휴일이면 다음 영업일로 미룸"""
    while is_holiday_or_weekend(d):
        d += dt.timedelta(days=1)
    return d

def compute_send_day(today: dt.date) -> int | None:
    """
    오늘 날짜(today)가 5/10/15를 주말·공휴일 보정한 '발송일'에 해당하면
    그 원래 기준일(5/10/15) 숫자를 반환. 아니면 None.
    """
    year, month = today.year, today.month
    for day in SCHEDULED_DAYS:
        try:
            base = dt.date(year, month, day)          # 이번 달 5/10/15
        except ValueError:
            # (예: 2월 30일 같은 불가능 날짜는 건너뜀)
            continue
        target = push_to_next_working_day(base)       # 주말/공휴일 보정
        if target == today:
            return day
    return None

# -------------------------------
# 2) 멘션/본문 템플릿
# -------------------------------
def get_mention(day: int) -> str:
    return {
        5:  "<@U02BG5HQZV4>",   # 권씨
        10: "<@U05B537RSJC>",   # 김씨
        15: "<@U050BP0GUNA>",   # 문씨
    }.get(day, "")

def get_text_for_5_or_15(day: int, mention: str) -> str | None:
    if day == 5:
        return f"""🗓️ {day}일 인증완료 배너 제작 요청일입니다! 아래 텍스트를 채워 해당 채널에 보내주세요! 강유나 멘션은 필수입니다! ❤️

1. 배너 목적 – 이 배너에서 강조하고자 하는 것이 무엇인가요? 최종 목적은 무엇인가요? (낮은 이자 대출 홍보, 보험 가입, 카드 발급 등)
2. 타겟 사용자 – 이 배너는 어떤 사용자에게 노출되나요? 어떤 사람들에게 노출되는 건가요? (예: 대출 심사를 받은 50대 등)
3. 메인 문구 – 가장 강조해야 하는 문장을 써주세요. 키워드로 작성해도 좋아요
4. 보조 문구 – 보조적으로 쓰이는 문장은? 쓰셨던 텍스트 요약해서 작성해줘도 좋아요
5. CTA (있다면) – 어떤 행동을 하길 원하는가요?
6. 디자인 참고자료 – 디자인에서 피해갈 요소가 있나요? (예: 특정 색상, 문구 등)
7. 희망 색상/톤:

👤 담당자: {mention}
"""
    if day == 15:
        return f"""🗓️ {day}일 대출비교 프로모션 배너 제작 요청일입니다! 아래 텍스트를 채워 해당 채널에 보내주세요! 강유나 멘션은 필수입니다! ❤️

1. 배너 목적 – 이 배너에서 강조하고자 하는 것이 무엇인가요? 최종 목적은 무엇인가요? (낮은 이자 대출 홍보, 보험 가입, 카드 발급 등)
2. 타겟 사용자 – 이 배너는 어떤 사용자에게 노출되나요? 어떤 사람들에게 노출되는 건가요? (예: 대출 심사를 받은 50대 등)
3. 메인 문구 – 가장 강조해야 하는 문장을 써주세요. 키워드로 작성해도 좋아요
4. 보조 문구 – 보조적으로 쓰이는 문장은? 쓰셨던 텍스트 요약해서 작성해줘도 좋아요
5. CTA (있다면) – 어떤 행동을 하길 원하는가요?
6. 디자인 참고자료 – 디자인에서 피해갈 요소가 있나요? (예: 특정 색상, 문구 등)
7. 희망 색상/톤:

👤 담당자: {mention}
"""
    return None

def send_for_day(day: int) -> None:
    """
    day가 10이면 2건, 5/15면 1건 발송.
    """
    mention = get_mention(day)

    # 10일: 두 개의 서로 다른 메시지 발송
    if day == 10:
        text1 = f"""🗓️ {day}일 앱 푸시 배너 제작 요청일입니다! 아래 텍스트를 채워 해당 채널에 보내주세요! 강유나 멘션은 필수입니다! ❤️

1. 배너 목적 – 이 배너에서 강조하고자 하는 것이 무엇인가요? 최종 목적은 무엇인가요? (낮은 이자 대출 홍보, 보험 가입, 카드 발급 등)
2. 타겟 사용자 – 이 배너는 어떤 사용자에게 노출되나요? 어떤 사람들에게 노출되는 건가요? (예: 대출 심사를 받은 50대 등)
3. 메인 문구 – 가장 강조해야 하는 문장을 써주세요. 키워드로 작성해도 좋아요
4. 보조 문구 – 보조적으로 쓰이는 문장은? 쓰셨던 텍스트 요약해서 작성해줘도 좋아요
5. CTA (있다면) – 어떤 행동을 하길 원하는가요?
6. 디자인 참고자료 – 디자인에서 피해갈 요소가 있나요? (예: 특정 색상, 문구 등)
7. 희망 색상/톤:
8. 제작할 내용 머니적립 or 금융광고 :

👤 담당자: {mention}
"""
        text2 = f"""🗓️ {day}일 KT외부 배너 제작 요청일입니다! 아래 텍스트를 채워 해당 채널에 보내주세요! 강유나 멘션은 필수입니다! ❤️

1. 배너 목적 – 이 배너에서 강조하고자 하는 것이 무엇인가요? 최종 목적은 무엇인가요? (낮은 이자 대출 홍보, 보험 가입, 카드 발급 등)
2. 타겟 사용자 – 이 배너는 어떤 사용자에게 노출되나요? 어떤 사람들에게 노출되는 건가요? (예: 대출 심사를 받은 50대 등)
3. 메인 문구 – 가장 강조해야 하는 문장을 써주세요. 키워드로 작성해도 좋아요
4. 보조 문구 – 보조적으로 쓰이는 문장은? 쓰셨던 텍스트 요약해서 작성해줘도 좋아요
5. CTA (있다면) – 어떤 행동을 하길 원하는가요?
6. 디자인 참고자료 – 디자인에서 피해갈 요소가 있나요? (예: 특정 색상, 문구 등)
7. 희망 색상/톤:

👤 담당자: {mention}
"""
        client.chat_postMessage(channel=CHANNEL_ID, text=text1)
        client.chat_postMessage(channel=CHANNEL_ID, text=text2)
        print("✅ 10일: 두 건 전송 완료")
        return

    # 5일/15일: 공통 템플릿 1건
    text = get_text_for_5_or_15(day, mention)
    if text:
        client.chat_postMessage(channel=CHANNEL_ID, text=text)
        print(f"✅ {day}일: 전송 완료")
    else:
        print(f"⚠️ {day}일: 전송 텍스트가 없습니다.")

# -------------------------------
# 3) 엔트리 포인트 (GitHub Actions)
# -------------------------------
if __name__ == "__main__":
    # 강제 발송용 입력 (GitHub Actions에서 입력으로 넘겨줌)
    force_day = os.getenv("FORCE_DAY")  # '5' / '10' / '15' 중 하나 또는 빈 값
    # 테스트 목적으로 오늘 날짜를 강제로 지정하고 싶으면 'YYYY-MM-DD'로 넘길 수 있게 옵션 제공(선택)
    force_today = os.getenv("FORCE_TODAY")  # 예: '2025-08-10'

    if force_today:
        try:
            today = dt.datetime.strptime(force_today, "%Y-%m-%d").date()
        except ValueError:
            raise RuntimeError("FORCE_TODAY 는 YYYY-MM-DD 형식이어야 합니다.")
    else:
        today = dt.date.today()

    if force_day:
        # 강제로 5/10/15 중 하나 지정되어 들어온 경우: 그냥 그 날짜용 메시지를 보냄
        try:
            day_num = int(force_day)
        except ValueError:
            raise RuntimeError("FORCE_DAY 는 5/10/15 중 하나의 숫자여야 합니다.")
        if day_num not in SCHEDULED_DAYS:
            raise RuntimeError("FORCE_DAY 는 5/10/15 중 하나여야 합니다.")
        send_for_day(day_num)
    else:
        # 평소 동작: 오늘이 발송일인지 계산해서 맞으면 발송
        scheduled_day = compute_send_day(today)
        if scheduled_day:
            send_for_day(scheduled_day)
        else:
            print("오늘은 발송일이 아닙니다. (또는 보정 결과가 오늘이 아님)")





# # ------------------------------------------ 2025.08.19 전 코드 
# from dotenv import load_dotenv
# import os
# import datetime
# from slack_sdk import WebClient



# # ✅ 슬랙 채널 ID 설정 (채널명 : 배너요정) 

# # CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID", "C08KRL1B4EB")
# # channel_id = "C08KRL1B4EB"


# # 테스트용 채널로 보내고 싶으면 아래 줄 주석 해제
# CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID", "C08L22G50CA")
# # channel_id = "C08L22G50CA"

# # ✅ 환경 변수 불러오기
# load_dotenv()
# slack_token = os.getenv("SLACK_TOKEN")
# client = WebClient(token=slack_token)



# # 👇 공휴일 리스트 (2025년 예시)
# KOREAN_HOLIDAYS = [
#     "2025-01-01", "2025-03-01", "2025-05-05", "2025-06-06", "2025-08-15",
#     "2025-10-03", "2025-12-25"
# ]

# scheduled_days = [5, 10, 15]
# today = datetime.date.today(2025, 8, 10)

# # ✅ 날짜가 주말 or 공휴일인지?
# def is_holiday_or_weekend(date):
#     return date.weekday() >= 5 or date.strftime("%Y-%m-%d") in KOREAN_HOLIDAYS

# def get_next_working_day(date):
#     # 👉 기준일 다음 날부터 확인
#     date += datetime.timedelta(days=1)
#     while is_holiday_or_weekend(date):
#         date += datetime.timedelta(days=1)
#     return date

# # ✅ 오늘이 메시지 보내는 날인지 확인
# def should_send_message():
#     for day in scheduled_days:
#         try:
#             base_date = today.replace(day=day)
#         except ValueError:
#             continue  # 2월 30일 같은 날짜 예외 처리
#         send_day = get_next_working_day(base_date) if is_holiday_or_weekend(base_date) else base_date
#         if send_day == today:
#             return day
#     return None

# # ✅ 담당자 멘션 자동 매칭
# def get_mention(day):
#     if day == 5:
#         return "<@U02BG5HQZV4>"  # 권씨 슬랙 ID
#     elif day == 10:
#         return "<@U05B537RSJC>"  # 김씨 슬랙 ID
#     elif day == 15:
#         return "<@U050BP0GUNA>"  # 문씨 슬랙 ID
#     return ""

# # ✅ 날짜별 텍스트 자동 매칭
# def get_text(day, mention):
#     if day == 5:
#         return f'''🗓️ {day}일 인증완료 배너 제작 요청일입니다! 아래 텍스트를 채워 해당 채널에 보내주세요! 강유나 멘션은 필수입니다! ❤️

# 1. 배너 목적 – 이 배너에서 강조하고자 하는 것이 무엇인가요? 최종 목적은 무엇인가요? (낮은 이자 대출 홍보, 보험 가입, 카드 발급 등)
# 2. 타겟 사용자 – 이 배너는 어떤 사용자에게 노출되나요? 어떤 사람들에게 노출되는 건가요? (예: 대출 심사를 받은 50대 등)
# 3. 메인 문구 – 가장 강조해야 하는 문장을 써주세요. 키워드로 작성해도 좋아요
# 4. 보조 문구 – 보조적으로 쓰이는 문장은? 쓰셨던 텍스트 요약해서 작성해줘도 좋아요
# 5. CTA (있다면) – 어떤 행동을 하길 원하는가요?
# 6. 디자인 참고자료 – 디자인에서 피해갈 요소가 있나요? (예: 특정 색상, 문구 등)
# 7. 희망 색상/톤:

# 👤 담당자: {mention}
# '''
#     elif day == 15:
#         return f'''🗓️ {day}일 대출비교 프로모션 배너 제작 요청일입니다! 아래 텍스트를 채워 해당 채널에 보내주세요! 강유나 멘션은 필수입니다! ❤️

# 1. 배너 목적 – 이 배너에서 강조하고자 하는 것이 무엇인가요? 최종 목적은 무엇인가요? (낮은 이자 대출 홍보, 보험 가입, 카드 발급 등)
# 2. 타겟 사용자 – 이 배너는 어떤 사용자에게 노출되나요? 어떤 사람들에게 노출되는 건가요? (예: 대출 심사를 받은 50대 등)
# 3. 메인 문구 – 가장 강조해야 하는 문장을 써주세요. 키워드로 작성해도 좋아요
# 4. 보조 문구 – 보조적으로 쓰이는 문장은? 쓰셨던 텍스트 요약해서 작성해줘도 좋아요
# 5. CTA (있다면) – 어떤 행동을 하길 원하는가요?
# 6. 디자인 참고자료 – 디자인에서 피해갈 요소가 있나요? (예: 특정 색상, 문구 등)
# 7. 희망 색상/톤:

# 👤 담당자: {mention}
# '''
#     return None

# # ✅ 메시지 보내기
# send_day = should_send_message()
# # 테스트 '배너요정 테스트 채널'로 보내고 싶으면 아래 코드 한 줄 주석 풀기 
# # send_day = 10


# if send_day == 10:
#     mention = get_mention(send_day)

#     # 메시지1
#     text1 = f"""🗓️ {day}일 앱 푸시 배너 제작 요청일입니다! 아래 텍스트를 채워 해당 채널에 보내주세요! 강유나 멘션은 필수입니다! ❤️
#                     1. 배너 목적 – 이 배너에서 강조하고자 하는 것이 무엇인가요? 최종 목적은 무엇인가요? (낮은 이자 대출 홍보, 보험 가입, 카드 발급 등)
#                     2. 타겟 사용자 – 이 배너는 어떤 사용자에게 노출되나요? 어떤 사람들에게 노출되는 건가요? (예: 대출 심사를 받은 50대 등)
#                     3. 메인 문구 – 가장 강조해야 하는 문장을 써주세요. 키워드로 작성해도 좋아요
#                     4. 보조 문구 – 보조적으로 쓰이는 문장은? 쓰셨던 텍스트 요약해서 작성해줘도 좋아요
#                     5. CTA (있다면) – 어떤 행동을 하길 원하는가요?
#                     6. 디자인 참고자료 – 디자인에서 피해갈 요소가 있나요? (예: 특정 색상, 문구 등)
#                     7. 희망 색상/톤:
#                     8. 제작할 내용 머니적립 or 금융광고 :


#                     👤 담당자: {mention}
#     """
#     client.chat_postMessage(channel=CHANNEL_ID, text=text1)

#     # 메시지2

#     text2 = f"""🗓️ {day}일 KT외부 배너 제작 요청일입니다! 아래 텍스트를 채워 해당 채널에 보내주세요! 강유나 멘션은 필수입니다! ❤️
#                 1. 배너 목적 – 이 배너에서 강조하고자 하는 것이 무엇인가요? 최종 목적은 무엇인가요? (낮은 이자 대출 홍보, 보험 가입, 카드 발급 등)
#                 2. 타겟 사용자 – 이 배너는 어떤 사용자에게 노출되나요? 어떤 사람들에게 노출되는 건가요? (예: 대출 심사를 받은 50대 등)
#                 3. 메인 문구 – 가장 강조해야 하는 문장을 써주세요. 키워드로 작성해도 좋아요
#                 4. 보조 문구 – 보조적으로 쓰이는 문장은? 쓰셨던 텍스트 요약해서 작성해줘도 좋아요
#                 5. CTA (있다면) – 어떤 행동을 하길 원하는가요?
#                 6. 디자인 참고자료 – 디자인에서 피해갈 요소가 있나요? (예: 특정 색상, 문구 등)
#                 7. 희망 색상/톤:

#                 👤 담당자: {mention}
#     """
#     client.chat_postMessage(channel=CHANNEL_ID, text=text2)
#     print("✅ 10일 두 건 전송 완료")
#     return


#  # 5일/15일
# text = get_text(day, mention)
# if text:
#     client.chat_postMessage(channel=CHANNEL_ID, text=text)
#     print(f"✅ {day}일 전송 완료")

# if __name__ == "__main__":
#     # 테스트/수동 실행용 강제 날짜 (예: 5/10/15)
#     force = os.getenv("FORCE_DAY")
#     day = int(force) if force else should_send_message()

#     if day in SCHEDULED_DAYS:
#         send_for_day(day)
#     else:
#         print("오늘은 발송일이 아닙니다. (또는 FORCE_DAY 미설정)")

# # import schedule
# # import time


# # 매일 아침 9시에 실행
# # schedule.every().day.at("10:30").do(run_bot)

# # print("⏰ 슬랙 메시지 봇이 실행 중입니다...")






