import unittest
from dataclasses import dataclass
from src.poker.card import Card, Rank, Suit
from src.poker.hand import Hand, Ranking


@dataclass
class TestHand:
    dealt: list[Card]
    hand: Hand
    
class TestCard(unittest.TestCase):

    def test_five_card_hands(self):
        hands : list[TestHand] = [
            TestHand(
                dealt=Card.from_str_list(["2c", "Jd", "8h", "Tc", "Kd"]),
                hand=Hand(
                    cards=Card.from_str_list(["Kd", "Jd", "Tc", "8h", "2c"]),
                    ranking=Ranking.HIGH_CARD,
                    description="king high"
                )
            ),
            TestHand(
                dealt=Card.from_str_list(["Ks", "As", "8h", "Tc", "Kd"]),
                hand=Hand(
                    cards=Card.from_str_list(["Ks", "Kd", "As", "Tc", "8h"]),
                    ranking=Ranking.PAIR,
                    description="pair of kings"
                )
            ),
            TestHand(
                dealt=Card.from_str_list(["Ks", "2s", "8h", "2c", "Kd"]),
                hand=Hand(
                    cards=Card.from_str_list(["Ks", "Kd", "2s", "2c", "8h"]),
                    ranking=Ranking.TWO_PAIR,
                    description="two pair kings and twos"
                )
            ),
            TestHand(
                dealt=Card.from_str_list(["7h","7d","5c","Tc","7c"]),
                hand=Hand(
                    cards=Card.from_str_list(["7h","7d", "7c", "Tc", "5c"]),
                    ranking=Ranking.THREE_OF_A_KIND,
                    description="three of a kind sevens"
                )
            ),
            TestHand(
                dealt=Card.from_str_list(["2h","4c","3s","5c","6h"]),
                hand=Hand(
                    cards=Card.from_str_list(["6h","5c", "4c", "3s", "2h"]),
                    ranking=Ranking.STRAIGHT,
                    description="straight six high"
                )
            ),
            TestHand(
                dealt=Card.from_str_list(["Ac","4c","3c","5c","6c"]),
                hand=Hand(
                    cards=Card.from_str_list(["Ac","6c", "5c", "4c", "3c"]),
                    ranking=Ranking.FLUSH,
                    description="flush ace high"
                )
            ),
            TestHand(
                dealt=Card.from_str_list(["6s","Jh","6c","6d","Jd"]),
                hand=Hand(
                    cards=Card.from_str_list(["6s","6c","6d","Jh","Jd"]),
                    ranking=Ranking.FULL_HOUSE,
                    description="full house sixes full of jacks"
                )
            ),
            TestHand(
                dealt=Card.from_str_list(["Ts","Jh","Td","Tc","Th"]),
                hand=Hand(
                    cards=Card.from_str_list(["Ts","Td","Tc","Th","Jh"]),
                    ranking=Ranking.FOUR_OF_A_KIND,
                    description="four of a kind tens"
                )
            ),
            TestHand(
                dealt=Card.from_str_list(["Ks","Qs","Js","9s","Ts"]),
                hand=Hand(
                    cards=Card.from_str_list(["Ks","Qs","Js","Ts","9s"]),
                    ranking=Ranking.STRAIGHT_FLUSH,
                    description="straight flush king high"
                )
            ),
            TestHand(
                dealt=Card.from_str_list(["Ks","Qs","Js","As","Ts"]),
                hand=Hand(
                    cards=Card.from_str_list(["As","Ks","Qs","Js","Ts"]),
                    ranking=Ranking.ROYAL_FLUSH,
                    description="royal flush"
                )
            ),
            TestHand(
                dealt=Card.from_str_list(["Ah","Ks","Ac","Tc","5s","9h","9s"]),
                hand=Hand(
                    cards=Card.from_str_list(["As","Ac","9h","9s","Ks"]),
                    ranking=Ranking.TWO_PAIR,
                    description="two pair aces and nines"
                )
            )
        ]
        for test_hand in hands:
            actual = Hand.from_cards(test_hand.dealt)
            self.assertEqual(test_hand.hand, actual)
    
    def test_hand_comparison(self):
        hand_1 = Hand.from_cards(Card.from_str_list(["2s","2c","Js","As","Ts"]))
        hand_2 = Hand.from_cards(Card.from_str_list(["2s","Kc","Js","As","Ts"]))
        self.assertLess(hand_2, hand_1)

if __name__ == '__main__':
    unittest.main()