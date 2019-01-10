"""
Compute average time to obtain desired Fallout 76 mutations using Monte-Carlo method.

There are currently 19 mutations available. Assume G are good (desired), B
are bad (undesired) and 19-(G+B) are don't care. Compute the average number
of Mutation events needed to get G-A good mutations and 0 bad mutations,
where A = 0,1,2 (because you can buy Mutation serums).

(C)2019 Robert Woodhead, trebor@animeigo.com. Released under GPL.
"""

from random import randrange, choice, seed
from statistics import mean

MUTATIONS = 19      # Number of possible mutations
MAX_SERUMS = 3      # Number of serums (targeted mutations) to allow
TRIALS = 1000       # Number of trials per permutation.

# Mutation state is encoded as a list of mutation numbers (0-based). If the number is
# < good, it's a good one, and if > bad, it's a bad one. We just use a list for
# simplicity, this isn't optimized code.


def mutate(state):
    """ Add a new mutation to the state and return the new state """

    mutation = randrange(MUTATIONS)
    while mutation in state:
        mutation = randrange(MUTATIONS)

    state.append(mutation)
    return state


def wash(state):
    """ Remove a random mutation from the state and return the new state """

    victim = choice(state)
    state.remove(victim)
    return state


def broad(good, bad, serums):
    """
    Mutate until we have good-serums good mutations and no bad ones.
    Remove mutations anytime we have a bad one.
    Return the number of mutations required.
    """

    state = []
    events = 0

    while True:

        events += 1

        state = mutate(state)

        goods = len([s for s in state if s < good])
        bads = len([s for s in state if s > bad])

        if goods >= (good - serums) and bads == 0:
            return events
        else:
            while bads > 0:
                state = wash(state)
                bads = len([s for s in state if s > bad])

            goods = len([s for s in state if s < good])
            if goods >= (good - serums):
                return events


def deep(good, bad, serums, state=[], events=0):
    """
    Mutate until we have good-serums good mutations and no bad ones.
    Remove bad mutations only after we have gotten all the required good ones.
    Return the number of mutations required.
    """

    state = []
    events = 0

    while True:

        events += 1

        state = mutate(state)

        goods = len([s for s in state if s < good])
        bads = len([s for s in state if s > bad])

        if goods >= (good - serums) and bads == 0:
            return events
        else:
            if goods < (good - serums):
                continue
            else:
                while bads > 0:
                    state = wash(state)
                    bads = len([s for s in state if s > bad])
                goods = len([s for s in state if s < good])
                if goods >= (good - serums):
                    return events


"""
Run all the trials for the permutations of required good mutations, bad mutations, and
serums. If, for example, a trial permits 2 serums then it will succeed if we get N-2
good mutations and no bad mutations.
"""

if __name__ == '__main__':
    seed()
    print('{}\t{}\t{}\t{}\t{}\t{}'.format('Good', 'Bad', 'Other', 'Serums', 'Broad', 'Deep'))

    for good in range(1, MUTATIONS):
        for bad in range(0, MUTATIONS + 1 - good):
            dontcare = MUTATIONS - (good + bad)
            badlimit = MUTATIONS - (bad + 1)
            for serums in range(0, MAX_SERUMS + 1):
                if serums < good:
                    avg_broad = mean([broad(good, badlimit, serums) for i in range(TRIALS)])
                    avg_deep = mean([deep(good, badlimit, serums) for i in range(TRIALS)])

                    print('{:d}\t{:d}\t{:d}\t{:d}\t{:f}\t{:f}'.format(good, bad, dontcare, serums, avg_broad, avg_deep))
