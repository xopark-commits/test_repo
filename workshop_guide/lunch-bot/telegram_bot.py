import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from sheets_manager import SheetsManager

# .env 파일 로드
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_message(text):
    """텔레그램으로 일반 텍스트 메시지를 보내는 함수"""
    if not CHAT_ID:
        print("❌ 에러: .env 파일의 TELEGRAM_CHAT_ID가 올바른 숫자 형식이 아닙니다.")
        return False
        
    bot = Bot(token=TOKEN)
    try:
        async with bot:
            await bot.send_message(chat_id=int(CHAT_ID), text=text)
            return True
    except Exception as e:
        print(f"❌ 메시지 전송 실패 (ID: {CHAT_ID}): {e}")
        return False

async def send_today_menu():
    """오늘의 점심 메뉴를 시트에서 가져와 포맷팅하여 전송하는 함수"""
    try:
        manager = SheetsManager()
        menus = manager.get_today_menus()
        
        if not menus:
            await send_message("📍 오늘은 등록된 점심 메뉴가 없습니다.")
            return
            
        text = "🍽 오늘의 점심 메뉴 투표 현황!\n\n"
        
        for i, item in enumerate(menus, 1):
            menu_name = item.get('메뉴', '이름 없음')
            category = item.get('카테고리', '-')
            proposer = item.get('제안자', '-')
            votes = item.get('투표수', 0)
            # 확정여부가 'O'인 경우 체크 표시 추가
            confirmed = " ✅ 확정" if str(item.get('확정여부')).upper() == "O" else ""
            
            text += f"{i}. {menu_name} ({category}) - 제안: {proposer} - 투표: {votes}표{confirmed}\n"
            
        success = await send_message(text)
        if success:
            print("✅ 텔레그램으로 메뉴 전송을 완료했습니다!")
        else:
            print("⚠️ 메뉴 전송에 실패했습니다. 봇이 차단되었거나 Chat ID가 올바른지 확인하세요.")
        
    except Exception as e:
        error_msg = f"❌ 메뉴 전송 중 오류 발생: {e}"
        print(error_msg)

if __name__ == "__main__":
    # 테스트 실행: 파일을 실행하면 즉시 텔레그램으로 메시지를 보냅니다.
    asyncio.run(send_today_menu())