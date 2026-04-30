# Phase 2 - 여기에 코드를 작성하세요
menu = {"치킨": 10000, "피자": 12000, "햄버거": 8000}

print("======= 배달 메뉴 =======")
for i in menu:
    print(i)
print(' 2개 이상 주문 시 10% 할인')
print("="*25)

final_list =[]
num_list =[]
menu_list =[]

for i in range(2):  #  반복 주문 

    menu_in = input("메뉴를 입력하세요: ")
    if menu_in in menu:
        num_in = input("수량을 입력하세요: ")
        if not num_in.isdigit():
            print("숫자를 입력해야 합니다.")
        else:
            # 가격 계산
            price_in = menu[menu_in]
            item_price = price_in * int(num_in)
            # 주문 리스트 추가 
            menu_list.append(menu_in)
            final_list.append(item_price)
            num_list.append(int(num_in))
            
            # 각 메뉴별 가격
            print(f"선택하신 {menu_in} 금액은 {item_price}원 입니다")
    else:
        print('없는 메뉴입니다.')

# 총 가격
total_price = sum(final_list)

# 할인 적용 
if sum(num_list) >=2:
    total_price = total_price * 0.9
    print(f" 2개이상 주문 하셨으므로 10% 할인이 적용됩니다.")
    
print(f"총 금액은 {total_price}원 입니다.") 

print("==== 주문내역 ====")
for i in range(len(menu_list)):
    if sum(num_list) >=2:
        print(f"{menu_list[i]} {num_list[i]}개 - {final_list[i] * 0.9}원 (할인적용)")
    else:
        print(f"{menu_list[i]} {num_list[i]}개 - {final_list[i]}원")








