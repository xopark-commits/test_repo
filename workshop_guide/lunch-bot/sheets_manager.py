import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from datetime import date

# 파일의 절대 경로를 기준으로 설정 파일(.env)을 찾습니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

class SheetsManager:
    def __init__(self):
        # 구글 API 인증 범위 설정
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # 설정값 로드 및 절대 경로 변환
        creds_filename = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
        self.creds_file = os.path.join(BASE_DIR, creds_filename)
        self.sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        
        if not os.path.exists(self.creds_file):
            raise FileNotFoundError(f"인증 파일을 찾을 수 없습니다: {self.creds_file}")

        # 구글 서비스 계정 인증
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_file, self.scope)
        self.client = gspread.authorize(self.creds)
        
        # 스프레드시트 열기 및 "점심메뉴" 워크시트 선택
        try:
            self.spreadsheet = self.client.open_by_key(self.sheet_id)
            self.sheet = self.spreadsheet.worksheet("점심메뉴")
        except gspread.exceptions.APIError as e:
            if "PERMISSION_DENIED" in str(e):
                print(f"❌ 권한 오류 발생! 구글 시트에서 아래 이메일을 '편집자'로 추가해 주세요:")
                print(f"👉 {self.creds.service_account_email}")
                raise PermissionError("구글 시트 공유 권한이 없습니다.")
            raise e
        except gspread.exceptions.WorksheetNotFound:
            # 시트 이름이 다를 경우를 대비해 첫 번째 시트를 기본값으로 사용
            self.sheet = self.spreadsheet.get_worksheet(0)

    def get_menus(self):
        """시트의 모든 데이터를 딕셔너리 리스트 형태로 가져옵니다."""
        return self.sheet.get_all_records()

    def get_today_menus(self):
        """오늘 날짜(2026-04-30)에 해당하는 메뉴만 필터링하여 가져옵니다."""
        today_str = date.today().strftime("%Y-%m-%d")
        all_menus = self.get_menus()
        # 시트의 '날짜' 컬럼과 오늘 날짜를 비교하여 필터링
        return [menu for menu in all_menus if str(menu.get('날짜')).strip() == today_str]

    def increase_vote(self, menu_name):
        """특정 메뉴의 투표수를 시트에서 직접 1 증가시킵니다."""
        try:
            # 헤더 목록을 가져와 '투표수'가 몇 번째 열인지 찾습니다.
            headers = self.sheet.row_values(1)
            vote_col = headers.index("투표수") + 1

            # 메뉴 이름이 있는 셀을 찾습니다.
            cell = self.sheet.find(menu_name)
            if cell:
                current_votes = self.sheet.cell(cell.row, vote_col).value
                # 숫자가 아닌 값이 있을 경우를 대비해 예외 처리
                try:
                    new_votes = int(current_votes) + 1 if current_votes else 1
                except (ValueError, TypeError):
                    new_votes = 1
                
                self.sheet.update_cell(cell.row, vote_col, new_votes)
                return new_votes
        except Exception as e:
            print(f"투표 반영 중 오류 발생: {e}")
        return None

if __name__ == "__main__":
    manager = SheetsManager()
    today_date = date.today().strftime("%Y-%m-%d")
    print(f"--- 오늘 날짜({today_date}) 메뉴 필터링 테스트 ---")
    
    today_menus = manager.get_today_menus()
    if today_menus:
        for i, menu in enumerate(today_menus, 1):
            print(f"{i}. {menu['메뉴']} ({menu['카테고리']}) - 투표수: {menu['투표수']}")
    else:
        print(f"현재 시트에 '{today_date}' 날짜의 데이터가 없습니다. 시트 데이터를 확인해 주세요.")