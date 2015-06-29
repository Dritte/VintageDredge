
"""
The following is an calculation of the probability of finding a 
4-of Bazaar of Baghdad in the opening hand of a 60 card Vintage 
Dredge Deck with 4 Serum Powders. This is combinatorial calculation, 
not a randomized simulation.

tl;dr Pr[Bazaar in opening hand] = 0.941681291934
      Pr[Bazaar by turn 1 on draw] = 0.946103359759
      Pr[Bazaar by turn 1 on draw with new mulligan rule] = 0.950266092187

by Eugenio Fortanely
 """

initial_hand_size = 7
initial_powders_in_library = 4
initial_library_size = 60
success_probabilities = {}
new_mull_rule = True
on_the_draw = True

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
  # if you've mulliganed to zero, you're done
  if hand_size <=0:
      if new_mull_rule and on_the_draw:
        return 1.0 - choose(library_size - 4, 2)*1.0/choose(library_size, 2)
      elif on_the_draw:
        return 1.0 - choose(library_size - 4, 1)*1.0/choose(library_size, 1)
      else:
          return 0.0
  # if you somehow have negative Serum Powders, you're done
  # this should never be true
  if powders_in_deck <= -1:
      raise
  # if you've managed to exile more than 28 cards you're done
  # this should never be true
  if library_size <= 31:
      raise
  # DP solution, memoize previous work
  if (hand_size, powders_in_deck, library_size) in success_probabilities:
    return success_probabilities[(hand_size, powders_in_deck, library_size)]

  probability_of_success = 0.0
  num_possible_hands_without_bazaar = (choose(library_size - 4, hand_size) * 1.0)
  num_possible_hands = choose(library_size, hand_size)
  probability_draw_bazaar =  \
    1.0 -  num_possible_hands_without_bazaar / num_possible_hands
  probability_of_success += probability_draw_bazaar
  for powders_drawn in range(powders_in_deck + 1):
    probability_no_bazaar_and_k_powder= \
      (choose(powders_in_deck, powders_drawn) * 1.0) * \
      choose(library_size - powders_in_deck - 4, hand_size - powders_drawn) / \
      choose(library_size, hand_size)
    probability_mulligan_success = \
      success_probability(hand_size - 1, powders_in_deck, library_size)                                                    
    if powders_drawn > 0:
      probability_powder_success = \
        success_probability(hand_size, powders_in_deck - powders_drawn, library_size - hand_size)
    else:
      probability_powder_success = 0.0
    ## Uncommenting the following lines will show for what combinations of hand 
    ## size, powders in deck and library size where a success is more likely by 
    ## mulliganing than using Serum Powder if a Serum Powder is drawn.
    ## Spoiler alert: It never is for a 60 card deck, but is neccessary for 
    ## completeness for very large library sizes that this program could be used to analyze.
    ##if powders_drawn > 0:
    ##  if probability_mulligan_success > probability_powder_success:
    ##    print "(hand_size, powders_in_deck, library_size)"
    ##    print (hand_size, powders_in_deck, library_size)
    ##    print "MULLIGAN"

    if hand_size < initial_hand_size and new_mull_rule and on_the_draw:
        probability_keep_success = 1.0 - choose(library_size - hand_size - 4, 2)*1.0/choose(library_size - hand_size, 2)
    elif hand_size < initial_hand_size and on_the_draw:
        probability_keep_success = 1.0 - choose(library_size - hand_size - 4, 1)*1.0/choose(library_size - hand_size, 1)
    else:
        probability_keep_success = 0.0
    ##if probability_keep_success > probability_powder_success and powders_drawn > 0:
    ##  print "(hand_size, powders_in_deck, library_size)"
    ##  print (hand_size, powders_in_deck, library_size)
    ##  print "probability_keep_success"
    ##  print probability_keep_success
    ##  print "probability_powder_success"
    ##  print probability_powder_success

    probability_of_success_if_you_draw_none_of_the_bazaar_and_k_serum_powder = \
      max([probability_mulligan_success, probability_powder_success,
          probability_keep_success])
    probability_of_success += \
      probability_no_bazaar_and_k_powder * probability_of_success_if_you_draw_none_of_the_bazaar_and_k_serum_powder

  success_probabilities[(hand_size, powders_in_deck, library_size)] = probability_of_success
  return probability_of_success

print success_probability(initial_hand_size, initial_powders_in_library, initial_library_size)

"""

Thanks to Daniel Kane for the following solution to solve this problem. 

Interesting problem. What you need there is dynamic programming. Let me explain:

If you want to compute the probability of getting the card from some
point onward, the probability of success depends on three things:
* How many times you've mulliganed so far (between 0 and 6 or 7
depending on whether you get a free mulligan)
* How many Serum Powders remain in your deck (between 0 and 4)
* How many other cards remain in your deck (between 60 and 32)

You want to compute the probability for all possible combinations of
parameters for these 3 variables (at most 1160 possible combinations,
so easy on a computer). Here's how you do it: The probability is
Probability that you draw one of the cards in your new hand +
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

OK. The first term is easy. You're drawing m cards out of n. There are
n choose m ways to do this. n-4 choose m have none of the 4-of, so the
probability that you succeed on the first draw is 1-(n-4 choose m)/(n
choose m).

For the other terms: What's the probability that you draw none of the
4-of and exactly k Serum powder?
Well, if you are drawing m cards from a deck of n and if there are h
Serum powder, the probability of drawing k and none of the 4-of is (h
choose k) * (n-h-4 choose m-k) / (n choose m)
[ h choose k for which serum powders you draw, n-h-4 choose m-k for
which other cards, divided by n choose m for the number of ways to
draw m cards ]

And then there's the probability of success given this draw. If you
drew 0 serum powders, you just mulligan, and look at the probability
of success with the same number of cards and serum powders but one
fewer mulligan left.
If you did draw a serum powder then there are two options. So you want
the maximum of the probabilities on 1: same number of cards and serum
powders but one fewer mulligan or 2: same number of mulligans but an
appropriate number of fewer cards and serum powders.

In any case this allows you to compute the answer for a given number
of cards/serum powders/mulligans left in terms of the answers in
situations where you have fewer of each. Thus you compute the answer
starting with the lowest possible number of each and work your way up.
"""
