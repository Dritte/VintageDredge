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

  probability_no_bazaar_and_k_powder = [0.0] * powders_in_deck
  
  for powders_drawn in range(powders_in_deck + 1):
    probability_no_bazaar_and_k_powder[powders_drawn] = choose(powders_in_deck, powders_drawn) * choose()

  probability_that_you_dont_and_draw_no_serum_powder = 0.0
  probability_of_success_if_you_draw_none_of_the_bazaar_and_no_serum_powder = 0.0 
  
  probability_that_you_dont_and_draw_one_serum_powder = 0.0
  probability_of_success_if_you_draw_none_of_the_bazaar_and_one_serum_powder = 0.0 
  
  probability_that_you_dont_and_draw_two_serum_powder = 0.0
  probability_of_success_if_you_draw_none_of_the_bazaar_and_two_serum_powder = 0.0 
  
  probability_that_you_dont_and_draw_three_serum_powder = 0.0
  probability_of_success_if_you_draw_none_of_the_bazaar_and_three_serum_powder = 0.0 
  
  probability_that_you_dont_and_draw_four_serum_powder = 0.0
  probability_of_success_if_you_draw_none_of_the_bazaar_and_four_serum_powder = 0.0 

  
