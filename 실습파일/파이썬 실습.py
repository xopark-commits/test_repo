
# 숫자를 문자열 키로 변경하여 0으로 시작할 수 있게 하고 중복을 제거했습니다.
telecom_list = {'010': 'SKT', '016': 'KT', '019': 'LGU'}

input_num = input("전화번호 : ")
input_tele = input_num[0:3] # int로 변환하지 않고 문자열 그대로 비교합니다.

if input_tele in telecom_list:
    print(f"당신은 {telecom_list[input_tele]} 사용자입니다.")
else:
    print("알 수 없는 통신사입니다.")






        
