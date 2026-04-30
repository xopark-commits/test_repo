import pandas as pd
import matplotlib.pyplot as plt

# 1. 데이터 생성 (2026년 추계 인구 데이터 포함)
data = {
    'City': ['서울', '부산', '대구', '인천', '광주'],
    'Sales': [1200, 800, 600, 900, 700],
    'Population': [930, 324, 235, 305, 139]  # 단위: 만 명
}
# 한글 깨짐 방지 설정 (Windows: Malgun Gothic)
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

df = pd.DataFrame(data)
# 1. Excel 데이터 로드 (파일 경로 확인 필요)
# .xls 파일을 읽기 위해 'xlrd' 라이브러리가 설치되어 있어야 합니다.
file_path = '1273485171_2.xls'
df = pd.read_excel(file_path)

# 2. 데이터 분석: 인구당 매출(Efficiency) 계산
df['Efficiency'] = df['Sales'] / df['Population']
# 2. 데이터 기본 확인 (상위 5행 및 요약 정보)
print("--- [데이터프레임 미리보기] ---")
print(df.head())
print("\n")

# 3. 데이터 정렬 (매출 순 및 효율 순)
df_sorted_sales = df.sort_values(by='Sales', ascending=False)
df_sorted_eff = df.sort_values(by='Efficiency', ascending=False)

# --- 분석 결과 출력 ---
print("--- [지역별 매출 분석 데이터프레임] ---")
print(df_sorted_sales)
print("--- [데이터 요약 정보] ---")
print(df.info())
print("\n")

# 4. 주요 통계 요약
total_sales = df['Sales'].sum()
avg_efficiency = df['Efficiency'].mean()
# 3. 데이터 분석 (예시: 인구당 매출 계산)
# 실제 엑셀의 컬럼명에 맞춰 'Sales', 'Population' 부분을 수정해야 합니다.
if 'Sales' in df.columns and 'Population' in df.columns:
    df['Efficiency'] = df['Sales'] / df['Population']
    df_sorted = df.sort_values(by='Efficiency', ascending=False)
    
    print("--- [효율성 분석 결과] ---")
    print(df_sorted[['City', 'Sales', 'Population', 'Efficiency']].head())

print(f"전체 총 매출: {total_sales:,}")
print(f"지역별 평균 효율: {avg_efficiency:.2f}")
print(f"최고 효율 지역: {df_sorted_eff.iloc[0]['City']} ({df_sorted_eff.iloc[0]['Efficiency']:.2f})")
print("-" * 40)

# 5. 시각화 (한글 깨짐 방지 설정이 필요할 수 있습니다)
plt.figure(figsize=(12, 5))

# 매출 규모 그래프
plt.subplot(1, 2, 1)
plt.bar(df_sorted_sales['City'], df_sorted_sales['Sales'], color='skyblue')
plt.title('City-wise Total Sales')
plt.ylabel('Sales Amount')

# 시장 효율성 그래프
plt.subplot(1, 2, 2)
plt.bar(df_sorted_eff['City'], df_sorted_eff['Efficiency'], color='salmon')
plt.title('Sales Efficiency (Sales/Population)')
plt.ylabel('Efficiency Score')

plt.tight_layout()
plt.show()
    # 4. 시각화
    plt.figure(figsize=(10, 5))
    plt.bar(df_sorted['City'], df_sorted['Efficiency'], color='salmon')
    plt.title('지역별 효율성 분석')
    plt.xlabel('지역')
    plt.ylabel('효율성 점수')
    plt.show()
else:
    print("Excel 파일에 'Sales' 또는 'Population' 컬럼이 존재하지 않습니다. 컬럼명을 확인해 주세요.")
    print(f"확인된 컬럼명: {df.columns.tolist()}")