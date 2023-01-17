import unittest
from src.poker.card import Card, Rank, Suit

class TestCard(unittest.TestCase):

    def test_card_str(self):
        card = Card(rank=Rank.ACE, suit=Suit.SPADES)
        self.assertEqual(str(card), 'A♠')

    def test_create_deck(self):
        cards = Card.deck()
        self.assertEqual(len(cards), 52)

if __name__ == '__main__':
    unittest.main()