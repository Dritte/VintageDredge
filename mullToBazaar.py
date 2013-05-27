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
  if hand_size <=0:
    return 0.0
  if powders_in_deck <= -1:
    return 0.0
  if library_size <= 31:
    return 0.0
  if (hand_size, powders_in_deck, library_size) in success_probabilities:
    return success_probabilities[(hand_size, powders_in_deck, library_size)]

  probability_of_success =  0.0

  probability_draw_bazaar = 1.0 - (choose(library_size - 4, hand_size) * 1.0) / choose(library_size, hand_size)

  probability_of_success += probability_draw_bazaar

  for powders_drawn in range(powders_in_deck + 1):
    probability_no_bazaar_and_k_powder= (choose(powders_in_deck, powders_drawn) * 1.0) * \
                                         (choose(library_size - powders_in_deck - 4, hand_size - powders_drawn) * 1.0 ) / \
                                         (choose(library_size, hand_size) * 1.0)

    probability_mulligan_success = success_probability(hand_size - 1, powders_in_deck, library_size)                                                    

    probability_power_success = success_probability(hand_size, powders_in_deck - powders_drawn, library_size - hand_size)

    probability_of_success_if_you_draw_none_of_the_bazaar_and_k_serum_powder = max(probability_mulligan_success, probability_power_success)

    probability_of_success+= (probability_no_bazaar_and_k_powder * probability_of_success_if_you_draw_none_of_the_bazaar_and_k_serum_powder)

  success_probabilities[(hand_size, powders_in_deck, library_size)] = probability_of_success
  return success_probabilities[(hand_size, powders_in_deck, library_size)]

print success_probability(7, 4, 60)
print len(success_probabilities)
  
