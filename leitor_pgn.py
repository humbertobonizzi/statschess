import chess
import chess.engine
import chess.pgn
import pandas as pd
from stockfish import Stockfish
from tqdm import tqdm
from datetime import datetime

print(datetime.now().strftime)

stockfish = Stockfish("/usr/local/bin/stockfish", depth=15, parameters={"Threads": 1, "Hash": 2048 })

def calcular_precisao(jogo):
    total_jogadas_brancas = 0
    jogadas_corretas_brancas = 0
    total_jogadas_negras = 0
    jogadas_corretas_negras = 0

    # Analisar a partida
    board = jogo.board()
    for movimento in jogo.mainline_moves():
        try:
            #Essa conversao nao esta funcionando.
            stockfish.set_fen_position(board.fen())
            melhor_jogada_stockfish = stockfish.get_best_move_time(100)

            #print("Jogada stockfish / Jogador")
            #print(melhor_jogada_stockfish , " / ", movimento)
        
            ehMelhorJogada = 1 if melhor_jogada_stockfish == str(movimento) else 0
            
            if board.turn:
                total_jogadas_brancas += 1
                jogadas_corretas_brancas += ehMelhorJogada
            else:
                total_jogadas_negras += 1
                jogadas_corretas_negras += ehMelhorJogada

            board.push(movimento)
        except Exception as e:
            print(repr(e))
            total_jogadas_brancas = 0
            total_jogadas_negras = 0
            jogadas_corretas_brancas = 0
            jogadas_corretas_negras = 0

    precisao_brancas = (jogadas_corretas_brancas / total_jogadas_brancas) * 100
    precisao_negras = (jogadas_corretas_negras / total_jogadas_negras) * 100
    #precisao_brancas = 30
    #precisao_negras = 30
    return [precisao_brancas, precisao_negras]

#Headers vindos do PGN
#Event='89th Hastings Masters 2013-14', 
#Site='Hastings ENG', 
#Date='2013.12.31', 
#Round='4.1', 
#White='Ma Qun', 
#Black='Gormally,D', 
#Result='1/2-1/2', 
#BlackElo='2500', 
#BlackFideId='406465', 
#BlackTitle='GM', 
#ECO='B90', 
#EventDate='2013.12.28', 
#Opening='Sicilian', 
#Variation='Najdorf, Byrne (English) attack', 
#WhiteElo='2595', 
#WhiteFideId='8603154', 
#WhiteTitle='GM')

#Colunas adicionais calcuadas
#QTD_JOGADAS
#precisao brancas
#Precisao NEgras

#Capturar o nome dos jogadores

lista_jogos = []

for i in range(920, 1498):
    with open(f"./base/twic{i}.pgn") as pgn:
        #print(f"twic{i}")
        while True:
            game = chess.pgn.read_game(pgn)
            if game is not None:
                jogo = {}
                jogo['evento'] = game.headers["Event"] if 'Event' in game.headers else ""
                jogo['data'] = game.headers["Date"] if 'Date' in game.headers else ""
                jogo['brancas'] = game.headers['White'] if 'White' in  game.headers else ""
                jogo['negras'] = game.headers['Black'] if 'Black' in game.headers else ""
                jogo['resultado'] = game.headers['Result'] if 'Result' in game.headers else ""
                jogo['FIDE_brancas'] = game.headers['WhiteFideId'] if 'WhiteFideId' in  game.headers else ""
                jogo['FIDE_negras'] = game.headers['BlackFideId'] if 'BlackFideId' in game.headers else ""
                jogo['elo_negras'] = game.headers['BlackElo'] if 'BlackElo' in game.headers else ""
                jogo['elo_brancas'] = game.headers['WhiteElo'] if 'WhiteElo' in game.headers else ""
                jogo['eco'] = game.headers['ECO'] if 'ECO' in game.headers else ""
                jogo['qtd_jogadas'] = int(len(list(game.mainline_moves()))/2)
                    
                print(game.headers['White'], ' vs', game.headers['Black'])

                precisao = calcular_precisao(game)
                print("Precisao")
                print(precisao)
                jogo['precisao_brancas'] = int(precisao[0])
                jogo['precisao_negras'] = int(precisao[1])

                lista_jogos.append(jogo)
            else:
                break
    break

df = pd.DataFrame(lista_jogos)
df.to_csv('jogos.csv', index=False, sep=';')

print(datetime.now)
