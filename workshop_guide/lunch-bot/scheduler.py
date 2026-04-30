import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram_bot import send_today_menu

# 로그 설정
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def main():
    # 1. 스케줄러 생성 (AsyncIO 환경용)
    scheduler = AsyncIOScheduler()

    # 2. 매일 오전 11시 00분에 send_today_menu 함수 실행 설정
    # 테스트를 위해 시간을 조정하려면 hour와 minute를 수정하세요.
    scheduler.add_job(send_today_menu, 'cron', hour=11, minute=0)

    print("🚀 스케줄러가 시작되었습니다. (매일 오전 11:00 알림)")
    print("🔔 테스트를 위해 지금 바로 메뉴를 1회 전송합니다...")
    
    # 시작하자마자 1회 즉시 실행 (테스트용)
    await send_today_menu()

    # 3. 스케줄러 시작
    scheduler.start()

    # 4. 프로그램이 종료되지 않도록 유지
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n👋 스케줄러를 종료합니다.")