import random
from typing import List
from collections import Counter
from argparse import ArgumentParser, Namespace

config = {
     # num of testcase
    'PATTERN_NUM': 1000,

    # Random seed
    'seed': 0,

    # Number of hands
    'num_hand': 5,

    # Tile type
    'tile_type' : 4,

    # Tile length
    'tile_len' : 6,

    # Tile max
    'tile_max_upper' : 15,

    # Probability of each tile
    'prob_honor'     : 0.1,
    'prob_character' : 0.3,
    'prob_bamboo'    : 0.3,
    'prob_dot'       : 0.3,
    'prob_unknown'   : 0.1,

    # Boundary of honor tiles (0d ~ 6d)
    'honor_lower': 0,
    'honor_upper': 6,

    # Boundary of character tiles, bamboo tiles and dot tiles (0d ~ 8d)
    'non_honor_lower': 0,
    'non_honor_upper': 8
}

random.seed(config['seed'])

honor_tiles     = '00'
character_tiles = '01'
bamboo_tiles    = '10'
dot_tiles       = '11'
unknown_tiles   = 'ff'

no_win            = '00'
unmentioned_tiles = '01'
sequence_win      = '10'
triplet_win       = '11'


def parse_args() -> Namespace:
    parser = ArgumentParser(description='DCSLab HW01 testdata generator')

    args = parser.parse_args()
    return args


def int2bin(num: int, len: int = 4) -> str:
    return f'{num:0{len}b}'


def bin2int(num_bin: str) -> int:
    return int(num_bin, 2)


def check_five_same(num: List[int]) -> bool:
    if len(num) != 5:
        return False
    
    if num[0] == num[1] and num[1] == num[2] and num[2] == num[3] and num[3] == num[4]:
        return True
    
    return False


def check_sequence(num: List[int]) -> bool:
    data = []
    for k, v in Counter(num).items():
        if v == 1:
            data.append(k)

    if len(data) != 3:
        return False 
    
    data = sorted(data)
    if data[0] + 1 == data[1] and data[1] + 1 == data[2]:
        return True

    return False 


def check_pair(num: List[int]) -> bool:
    for _, v in Counter(num).items():
        if v == 2:
            return True
        
    return False 


def check_triplet(num: List[int]) -> bool:    
    for _, v in Counter(num).items():
        if v == 3:
            return True
        
    return False 


def sol(hand_tiles: str) -> str:
    tiles = []
    for i in range(config['num_hand']):
        tiles.append(hand_tiles[i * config['tile_len'] : (i + 1) * config['tile_len']])

    tiles_dict = {
        honor_tiles     : [],
        character_tiles : [],
        bamboo_tiles    : [],
        dot_tiles       : [],
        unknown_tiles   : []
    }

    tiles_num_dict = {
        honor_tiles     : 0,
        character_tiles : 0,
        bamboo_tiles    : 0,
        dot_tiles       : 0,
        unknown_tiles   : 0
    }

    for tile in tiles:
        tile_type = tile[:2]
        tile_value = bin2int(tile[2:])

        if tile_type == honor_tiles and tile_value <= config['honor_upper']:
            tiles_dict[honor_tiles].append(tile_value)
            tiles_num_dict[honor_tiles] += 1
        elif tile_type == character_tiles and tile_value <= config['non_honor_upper']:
            tiles_dict[character_tiles].append(tile_value)
            tiles_num_dict[character_tiles] += 1
        elif tile_type == bamboo_tiles and tile_value <= config['non_honor_upper']:
            tiles_dict[bamboo_tiles].append(tile_value)
            tiles_num_dict[bamboo_tiles] += 1
        elif tile_type == dot_tiles and tile_value <= config['non_honor_upper']:
            tiles_dict[dot_tiles].append(tile_value)
            tiles_num_dict[dot_tiles] += 1
        else:
            tiles_dict[unknown_tiles].append(tile_value)
            tiles_num_dict[unknown_tiles] += 1

    if tiles_num_dict[unknown_tiles] > 0:
        return unmentioned_tiles
    
    if check_five_same(tiles_dict[honor_tiles]) or \
       check_five_same(tiles_dict[character_tiles]) or \
       check_five_same(tiles_dict[bamboo_tiles]) or \
       check_five_same(tiles_dict[dot_tiles]):
        return unmentioned_tiles

    pair_tile_type = None
    triplet_tile_type = None
    for key, val in tiles_num_dict.items():
        if val == 2:
            pair_tile_type = key
        
        if val == 3:
            triplet_tile_type = key

        if val == 5:
            pair_tile_type = key
            triplet_tile_type = key

    if pair_tile_type and triplet_tile_type:
        if check_sequence(tiles_dict[triplet_tile_type]) and check_pair(tiles_dict[pair_tile_type]):
            return sequence_win

        if check_triplet(tiles_dict[triplet_tile_type]) and check_pair(tiles_dict[pair_tile_type]):
            return triplet_win

    return no_win 


def gen_test_data(input_file_path: str, output_file_path: str) -> None:    
    pIFile = open(input_file_path, 'w')
    pOFile = open(output_file_path, 'w')

    PATTERN_NUM = config['PATTERN_NUM']

    tile_weight = [
        config['prob_honor'],
        config['prob_character'],
        config['prob_bamboo'],
        config['prob_dot'],
        config['prob_unknown']
    ]

    stat_dict = {
        no_win     : 0,
        unmentioned_tiles : 0,
        sequence_win    : 0,
        triplet_win       : 0
    }

    for _ in range(PATTERN_NUM):
        hand_tiles = ""
        for _ in range(config['num_hand']):
            tile_type = random.choices(list(range(config['tile_type'] + 1)), weights=tile_weight)[0]
            
            if tile_type == 0:
                tile = random.randint(config['honor_lower'], config['honor_upper'])
                tile_str = int2bin(tile) + honor_tiles
            else:
                tile = random.randint(config['non_honor_lower'], config['non_honor_upper'])
                if tile_type == 1:
                    tile_str = character_tiles + int2bin(tile)
                elif tile_type == 2:
                    tile_str = bamboo_tiles + int2bin(tile)
                elif tile_type == 3:
                    tile_str = dot_tiles + int2bin(tile) 
                elif tile_type == 4:
                    if random.random() < 0.5:
                        tile = random.randint(config['honor_upper'] + 1, config['tile_max_upper'])
                        tile_str = honor_tiles + int2bin(tile)
                    else:
                        tile = random.randint(config['non_honor_upper'] + 1, config['tile_max_upper'])
                        non_honor_tile = random.randint(1, 3)
                        tile_str = int2bin(non_honor_tile, 2) + int2bin(tile)
                else:
                    print("Tile type error!")
            
            if len(tile_str) != config['tile_len']:
                print("Tile length error!")

            hand_tiles += tile_str
        pIFile.write(f"{hand_tiles}\n")
        result = sol(hand_tiles)
        stat_dict[result] += 1
        pOFile.write(f'{result}\n')

    print(stat_dict)

    pIFile.close()
    pOFile.close()


def main(args: Namespace) -> None:
    gen_test_data("input.txt", "output.txt")


if __name__ == '__main__':
    args = parse_args()
    main(args)