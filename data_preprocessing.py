import numpy as np
import chess.pgn
from tqdm import tqdm

import pandas as pd

def get_first_k_moves(use_username = True, username= None, path = None, max_games = 100000):
    if username == None and path == None:
        return "Error please specify either username or path to pgn"
    if use_username:
        filename = f'games_{username}.pgn'
        path = f'games/{filename}'
    pgn = open(path)
    df = pd.DataFrame(columns = ['planes','White','WhiteElo','Black','BlackElo','date'])
    n = 1
    for n in tqdm(range(max_games)):
        game = chess.pgn.read_game(pgn)
        #print(game)
        if game == None:
            break
        n+=1
        white_name = game.headers["White"]
        black_name = game.headers["Black"]
        white_elo = game.headers["WhiteElo"]
        black_elo = game.headers["BlackElo"]
        eco = game.headers["ECO"]
        opening = game.headers["Opening"]
        date = game.headers["Date"]
        result = game.headers["Result"]

        if white_name !='' and black_name !='' and white_elo not in ['','?'] and black_elo not in ['','?']:
            planes = []
            moves = game.mainline_moves()
            for move in moves:
                planes.append(str(move))

            row = pd.DataFrame({
                'planes': [planes],
                'White': white_name,
                'Black': black_name,
                'no_of_moves': len(planes),
                'result': result,
                'WhiteElo': int(white_elo),
                'BlackElo': int(black_elo),
                'date': date, 
                'eco': eco, 
                'opening': opening
            })
            df = pd.concat([df,row])
    return df

import os

def get_concat_moves(dir, max_games = 100000):
    list_of_df = []

    for game_file in os.listdir(dir):
        path = f'./{dir}/{game_file}'
        new_df = get_first_k_moves(use_username = False, path = path, max_games = max_games)
        list_of_df.append(new_df)
    return pd.concat(list_of_df)

import pickle

dir = input("Enter directory name: ")
max_games = int(input("Enter max number of games: "))

df = get_concat_moves(dir, max_games)

filename = f'df_{dir}_{max_games}.dat'
outfile = open(filename,'wb')
pickle.dump(df, outfile)
outfile.close()