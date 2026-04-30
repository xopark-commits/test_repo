print ("=== 배달 메뉴 ===")
print ("1. 치킨 (10000원)")
print ("2. 피자 (12000원)")
print ("3. 햄버거 (8000원)")
print ("=================")

orders_txt = ""
total_sum = 0

for i in range(2):
    print(f"\n{i + 1}번째 주문")

    food = input("메뉴를 입력하세요: ")
    count = int(input("수량을 입력하세요: "))

    if food == "치킨" : 
        price = 10000
    elif food == "피자" :
        price = 12000
    elif food == "햄버거" :
        price = 8000
    else :
        print("없는 메뉴입니다.")
        continue

    original = price * count
    discount = 0

    if count >= 2:
        discount = int(original * 0.1)
        total = original - discount
        line = f"({food} {count}개 - {total}원 (할인 적용))"
    else:
        total = original
        line = f"({food} {count}개 - {total}원)"
    
    total_sum += total
    orders_txt += line + "\n"


print("\n=== 주문 내역 ===")
print(orders_txt)

print(f"총 결제 금액 : {total_sum}원")
print("=================")