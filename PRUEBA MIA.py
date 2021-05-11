def disponer_ladrillos():
    level1 = ['XXXXXXXX', 
                'X--DD--X', 
                'X--DD--X', 
                'XXXXXXXX'] 
    column = 0
    filaint = 0
    grupoLadrilos = []

    for fila in level1:
        y = filaint *40 + 5
        for caracter in fila:
            x = column * 100 + 5
            if caracter == 'X':
                ladrillo = 4
            elif caracter == 'D':
                ladrillo= 5
            else:
                pass
            grupoLadrilos.append(ladrillo)
            
    print (grupoLadrilos)
    
disponer_ladrillos()    
            

