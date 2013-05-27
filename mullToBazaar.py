success_probabilities = {}

def choose(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in xrange(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

def success_probability(hand_size, powders_in_deck, library_size):
  if (hand_size, powders_in_deck, library_size) in success_probabilities:
    return success_probabilities[(hand_size, powders_in_deck, library_size)]
  probability_draw_bazaar = 1.0 - (choose(library_size - 4, hand_size) * 1.0) / choose(library_size, hand_size)

(Probability that you don't and draw no Serum Powder) * (Probability
of success if you draw non of the 4-of and no Serum powder) +
(Probability that you don't and draw one Serum Powder) * (Probability
of success if you draw non of the 4-of and one Serum powder) +
(Probability that you don't and draw two Serum Powder) * (Probability
of success if you draw non of the 4-of and two Serum powder) +
(Probability that you don't and draw three Serum Powder) *
(Probability of success if you draw non of the 4-of and three Serum
powder) + (Probability that you don't and draw four Serum Powder) *
(Probability of success if you draw non of the 4-of and four Serum
powder).
