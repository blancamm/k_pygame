def edad_buena(valor):
    try:
        v=int(valor)
        if v<1:
            return False
        return True
    except:
        return False


edad = input('Dime tu edad: ')

while not edad_buena(edad):
    edad = input('mal, otra vez:')
