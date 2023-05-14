def fibonacci(n):
    return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)


if __name__ == '__main__':
    valor = int(input("Enter an integer: "))
    print(f'fibonacci: {fibonacci(valor)}')