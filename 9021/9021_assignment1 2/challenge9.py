for a in range(10, 77):
    a_number = [a // 10, a % 10]
    if len(a_number) != 2:
        continue
    for b in range(a+1, 88):
        b_number = [b // 10, b % 10]
        a_and_b_number = a_number + b_number
        if len(set(a_and_b_number)) != 4:
            continue
        for c in range(b+1, 99):
            c_number = [c // 10, c % 10]
            a_and_b_c_number = a_and_b_number + c_number
            if len(set(a_and_b_c_number)) != 6:
                continue
            product = a * b * c
            total_number = []
            for i in range(0, len(str(product))):
                total_number.append(int(list(str(product))[i]))
            if set(total_number) == set(a_and_b_c_number):
                print(f'{a} x {b} x {c} = {product} is a solution.')

