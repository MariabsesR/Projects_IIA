def func_32(estado,jogador):

    f1 = 0.05
    f2 = 1
    f3 = 0.05
    f4 = 0.7
    f5 = 0.1
    f6 = 0.12
    
    sementes_sul = 0
    sementes_norte = 0
    vazios_sul = 0
    vazios_norte = 0
    sementes_possiveis_capturar_sul = 0
    sementes_possiveis_capturar_norte = 0

    biggest_loss_south = 0
    biggest_loss_north = 0
    
    for i in range(len(estado.state)):
        estado_atingido = estado.state[(i + estado.state[i]) % 13]

        if i < 6:
            sementes_sul+=estado.state[i]
            if estado.state[i] == 0:
                vazios_sul+=1
        elif i > 6 and i < 13:
            sementes_norte+=estado.state[i]
            if estado.state[i] == 0:
                vazios_norte+=1

        if estado_atingido == 0 and i<6 and (i + estado.state[i]) % 13 != estado.SOUTH_SCORE_PIT and i != (i + estado.state[i]) % 13 and (i + estado.state[i]) % 13 < 6:
            depois_captura = (i + estado.state[i]) % 13
            sementes_capturaveis = estado.state[(len(estado.state) - 1- depois_captura -1)%13] + 1
            sementes_possiveis_capturar_sul += sementes_capturaveis

            if sementes_capturaveis > biggest_loss_north:
                biggest_loss_north = sementes_capturaveis
        
        elif estado_atingido == 0 and i>6 and i<13 and (i + estado.state[i]) % 13 != estado.NORTH_SCORE_PIT and i != (i + estado.state[i]) % 13 and (i + estado.state[i]) % 13 > 6:
            depois_captura = (i + estado.state[i]) % 13
            sementes_capturaveis = estado.state[(len(estado.state) - 1- depois_captura -1)%13] + 1
            sementes_possiveis_capturar_norte += estado.state[(len(estado.state) - 1- depois_captura -1)%13] + 1

            if sementes_capturaveis > biggest_loss_south:
                biggest_loss_south = sementes_capturaveis
    
    
    if jogador == estado.SOUTH:
        resultado = f1*(sementes_sul-sementes_norte) + f2*(estado.state[estado.SOUTH_SCORE_PIT]-estado.state[estado.NORTH_SCORE_PIT]) + f3*(sementes_possiveis_capturar_sul - sementes_possiveis_capturar_norte) - f6*biggest_loss_south
    else:
        resultado = f1*(sementes_norte-sementes_sul) + f2*(estado.state[estado.NORTH_SCORE_PIT]-estado.state[estado.SOUTH_SCORE_PIT]) + f3*(sementes_possiveis_capturar_norte - sementes_possiveis_capturar_sul) - f6*biggest_loss_north
    
    if jogador != estado.to_move and estado.pass_turn:
        resultado += f4
    
    if jogador == estado.SOUTH and estado.state[estado.SOUTH_SCORE_PIT] > sementes_norte + estado.state[estado.NORTH_SCORE_PIT]:
        resultado+= f5* (vazios_sul-vazios_norte)
    elif jogador == estado.NORTH and estado.state[estado.NORTH_SCORE_PIT] > sementes_sul + estado.state[estado.SOUTH_SCORE_PIT]:
        resultado += f5*(vazios_norte - vazios_sul)
    return resultado
