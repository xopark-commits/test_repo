import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from sheets_manager import SheetsManager

# .env 파일 로드
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 로그 설정 (오류 확인용)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start 명령어 처리: 사용자에게 인사와 Chat ID를 안내합니다."""
    user_id = update.effective_chat.id
    await update.message.reply_text(
        f"안녕하세요! 점심 메뉴 알림 봇입니다.\n"
        f"당신의 Chat ID는 {user_id} 입니다.\n"
        f"/lunch 명령어를 입력하면 메뉴를 확인하실 수 있습니다."
    )

async def send_lunch_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/lunch 명령어 처리: 구글 시트에서 메뉴를 읽어와 전송합니다."""
    try:
        manager = SheetsManager()
        menus = manager.get_menus()
        
        if not menus:
            await update.message.reply_text("📍 현재 등록된 메뉴 데이터가 없습니다.")
            return
            
        text = "🍱 오늘의 점심 메뉴 목록 🍱\n\n"
        for i, item in enumerate(menus, 1):
            # 시트의 헤더(컬럼명)를 기반으로 메시지를 구성합니다.
            details = " | ".join([f"{k}: {v}" for k, v in item.items()])
            text += f"{i}. {details}\n"
            
        await update.message.reply_text(text)
    except Exception as e:
        await update.message.reply_text(f"❌ 메뉴를 불러오는 중 오류 발생: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('lunch', send_lunch_menu))
    
    print("🚀 봇이 가동되었습니다. 텔레그램 앱에서 /lunch 를 입력해 보세요!")
    application.run_polling()