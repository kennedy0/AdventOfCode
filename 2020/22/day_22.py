import copy
import sys
from typing import List, Tuple

from utils.input_file import file_path_from_args
from utils.read_lines import read_lines


def main(input_file: str) -> int:
    player_1, player_2 = parse_decks(file=input_file)
    play_combat([int(i) for i in player_1], [int(i) for i in player_2])
    play_recursive_combat([int(i) for i in player_1], [int(i) for i in player_2])
    return 0


def parse_decks(file: str) -> Tuple[List, List]:
    lines = list(read_lines(file_path=file))
    index = lines.index("")
    deck_1 = lines[1:index]
    deck_2 = lines[index+2:]
    return deck_1[::-1], deck_2[::-1]


def play_round(player_1: List, player_2: List):
    card_1 = player_1.pop()
    card_2 = player_2.pop()
    if card_1 > card_2:
        player_1.insert(0, card_1)
        player_1.insert(0, card_2)
    else:
        player_2.insert(0, card_2)
        player_2.insert(0, card_1)


def play_recursive_round(player_1: List, player_2: List):
    card_1 = player_1.pop()
    card_2 = player_2.pop()

    if len(player_1) >= card_1 and len(player_2) >= card_2:
        print('recursive!!!')
        winner = play_recursive_combat(player_1=copy.copy(player_1[-card_1:]), player_2=copy.copy(player_2[-card_2:]))
    elif card_1 > card_2:
        winner = 1
    else:
        winner = 2

    if winner == 1:
        player_1.insert(0, card_1)
        player_1.insert(0, card_2)
    else:
        player_2.insert(0, card_2)
        player_2.insert(0, card_1)


def calculate_score(deck: List) -> int:
    score = 0
    for i, card in enumerate(deck, start=1):
        score += i * card
    return score


def play_combat(player_1: List, player_2: List):
    rounds = 0
    while min([len(player_1), len(player_2)]) > 0:
        play_round(player_1, player_2)
        rounds += 1

    if len(player_1):
        winner = "Player 1"
        score = calculate_score(deck=player_1)
    else:
        winner = "Player 2"
        score = calculate_score(deck=player_2)

    print(f"{winner} wins Combat after {rounds} rounds. Score: {score}")


def play_recursive_combat(player_1: List, player_2: List, game_number: int = 1) -> int:
    history = []
    winner = None
    rounds = 0
    while min([len(player_1), len(player_2)]) > 0:
        if [player_1, player_2] in history:
            winner = 1
            break
        else:
            history.append([copy.copy(player_1), copy.copy(player_2)])
        play_recursive_round(player_1, player_2)
        rounds += 1

    if winner is None:
        if len(player_1):
            winner = 1
        else:
            winner = 2

    if winner == 1:
        score = calculate_score(deck=player_1)
    else:
        score = calculate_score(deck=player_2)

    print(f"Player {winner} wins Recursive Combat after {rounds} rounds. Score: {score}")
    return winner


if __name__ == "__main__":
    sys.exit(main(file_path_from_args()))
