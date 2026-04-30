# === 카페 메뉴 ===
# 아메리카노
# 라떼
# 케이크

# 메뉴를 입력하세요: 아메리카노
# 수량을 입력하세요: 2

# 총 금액은 6000원 입니다.

menu = {"아메리카노": 3000, "라떼": 4000, "케이크": 5000}

def show_menu():
    print("=== 카페 메뉴 ===")
    for i in menu:
        print(i)



show_menu()
final_list =[]
for i in range(3):  # 3번 반복 주문 

    menu_in = input("메뉴를 입력하세요: ")
    if menu_in in menu:
        num_in = input("수량을 입력하세요: ")
        if not num_in.isdigit():
            print("숫자를 입력해야 합니다.")
        else:
            price_in = menu[menu_in]
            final_price = price_in * int(num_in)
            final_list.append(final_price)
            print(f"선택하신 {menu_in} 금액은 {final_price}원 입니다")
    else:
        print('없는 메뉴입니다.')

total_price = sum(final_list)
print(f"총 금액은 {total_price}원 입니다.") 







