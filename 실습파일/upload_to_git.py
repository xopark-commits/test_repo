import subprocess
import os
import sys
import io

# 한글 출력 깨짐 방지
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def run_git_upload():
    target_dir = r"C:\Users\20228\Downloads\xopark_project"
    repo_url = "https://github.com/xopark-commits/test_repo.git"
    
    # 1. 사용자 정보 설정 (요청하신 이메일 반영)
    user_email = "xo.park@gmail.com"
    user_name = "xopark-commits" # 이름은 닉네임으로 설정

    if not os.path.exists(target_dir):
        print(f"❌ 경로 없음: {target_dir}")
        return

    os.chdir(target_dir)

    try:
        print(f"📂 작업 위치: {os.getcwd()}")

        # 2. Git 사용자 정보 등록 (시스템 설정)
        print("👤 Git 사용자 정보를 설정합니다...")
        subprocess.run(f'git config --global user.email "{user_email}"', shell=True, check=True)
        subprocess.run(f'git config --global user.name "{user_name}"', shell=True, check=True)

        # 3. .gitignore 파일 생성 (대용량 파일 제외)
        # 이미 존재하면 덮어쓰고, 용량이 큰 파일을 목록에 추가합니다.
        print("🚫 대용량 파일 업로드 제외 설정 중...")
        ignore_content = [
            "판다스/market_2017.csv",
            "판다스/market_2022.csv",
            "workshop_guide/lunch-bot/credentials.json",
            "*.ipynb_checkpoints/"  # 불필요한 체크포인트 폴더도 제외 권장
        ]
        with open(".gitignore", "w", encoding="utf-8") as f:
            f.write("\n".join(ignore_content))

        # 4. Git 초기화 및 기존 기록 삭제 (용량 문제 해결을 위해 다시 시작)
        if os.path.exists(".git"):
            # 윈도우 명령어로 .git 폴더 강제 삭제 (기존에 꼬인 기록 제거)
            subprocess.run("rmdir /s /q .git", shell=True)
        
        print("🚀 Git 초기화 중...")
        subprocess.run("git init", shell=True, check=True)
        
        # 5. 모든 파일 추가 및 커밋
        print("📝 파일 추가 중 (큰 파일 제외)...")
        subprocess.run("git add .", shell=True, check=True)
        
        print("💾 커밋 기록 중...")
        subprocess.run('git commit -m "Initial upload without large files"', shell=True, check=True)
        
        # 6. 브랜치 및 원격 저장소 연결
        subprocess.run("git branch -M main", shell=True, check=True)
        print("🔗 GitHub 연결 설정...")
        subprocess.run(f"git remote add origin {repo_url}", shell=True)
            
        # 7. 푸시 (Push)
        print("☁️ GitHub 전송 시작... (브라우저 인증창이 뜨면 확인해 주세요)")
        # -f를 써서 깨끗하게 새로 만든 기록을 밀어넣습니다.
        result = subprocess.run("git push -f -u origin main", shell=True)
        
        if result.returncode == 0:
            print("\n✅ 성공: 큰 파일을 제외한 모든 파일이 GitHub에 업로드되었습니다!")
        else:
            print("\n❌ 푸시 실패: 위 메시지를 확인해 주세요.")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

if __name__ == "__main__":
    run_git_upload()