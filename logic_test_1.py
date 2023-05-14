def fizz_buzz(n):
    """fizz buzz function"""
    if (n % 3 == 0) and (n % 5 == 0):
        return 'fizz buzz'
    if (n % 5 == 0):
        return 'buzz'
    if (n % 3 == 0):
        return 'fizz'
    return str(n)


if __name__ == '__main__':
    for n in range(1,101):
        print(fizz_buzz(n))