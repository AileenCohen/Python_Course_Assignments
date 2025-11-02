def create_area_calculator(height, base):
    return f'The area of the triangle is: {(height * base) / 2}'

a = float(input("Enter the height of the triangle: "))
b = float(input("Enter the base of the triangle: "))
print(create_area_calculator(a,b))