#!/usr/bin/env python3

"""A simple python script template.
"""

import os
import sys
import argparse
from src.poker.card import Card
from src.poker.table import Table, Seat, Action

def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # parser.add_argument('infile', help="Input file", type=argparse.FileType('r'))
    # parser.add_argument('-o', '--outfile', help="Output file",
    #                     default=sys.stdout, type=argparse.FileType('w'))
    args = parser.parse_args(arguments)

    table = Table.start()
    while True:
        print_table(table=table)
        action_str = input("Enter your action (f,c,r): ")
        match action_str:
            case "f":
                table.action(action=Action.Fold)
            case "c":
                table.action(action=Action.CheckCall)
            case "r":
                table.action(action=Action.BetRaise)

def print_table(table: Table):
    for seat in [Seat.One, Seat.Two]:    
        p = table.seats[seat]
        p.hole_cards.sort(reverse=True)
        button_str = "B" if seat == table.button else ""
        print(f"{seat}: Chips {p.chips} Cards {cards_str(p.hole_cards)} {button_str}")
    print(f"{table.round} - {table.turn} - Pot {table.pot} {cards_str(table.board)}")

def cards_str(cards: list[Card])  -> str:
    return "".join(list(map(lambda c: str(c), cards)))

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))