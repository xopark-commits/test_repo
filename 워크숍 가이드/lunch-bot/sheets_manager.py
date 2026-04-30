import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# 파일의 절대 경로를 기준으로 설정 파일을 찾도록 개선
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

class SheetsManager:
    def __init__(self):
        # 구글 API 인증을 위한 권한 범위(scope) 설정
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # 설정값 로드
        creds_filename = os.getenv("GOOGLE_CREDENTIALS_FILE")
        self.creds_file = os.path.join(BASE_DIR, creds_filename) if creds_filename else None
        self.sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        
        if not self.creds_file or not os.path.exists(self.creds_file):
            raise FileNotFoundError(f"인증 파일을 찾을 수 없습니다: {self.creds_file}")

        # 구글 서비스 계정 인증
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_file, self.scope)
        self.client = gspread.authorize(self.creds)
        
        # 스프레드시트 열기 (첫 번째 워크시트 선택)
        self.sheet = self.client.open_by_key(self.sheet_id).sheet1

    def get_menus(self):
        """시트의 모든 데이터를 딕셔너리 리스트 형태로 가져옵니다."""
        return self.sheet.get_all_records()

if __name__ == "__main__":
    # 테스트 실행
    manager = SheetsManager()
    data = manager.get_menus()
    print("--- 스프레드시트 데이터 확인 ---")
    for row in data:
        print(row)