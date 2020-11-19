"""
Implementation of helper functions for the realization of the critic method.

Source: D. Diakoulaki, G. Mavrotas, and L. Papayannakis:
        „Determining objective weights in multiple criteria problems: The CRITIC method“,
        Comput. Oper. Res., Bd. 22, Nr. 7, S. 763–770, 1995.
"""
from django.db.models import Avg, Max, Min
import operator
import logging

from solutions import models as solution_models

logger = logging.getLogger(__name__)


def normalize(solution_space: solution_models.SolutionSpace,
              permutation: solution_models.Permutation,
              attribute: str,
              max_best: bool = False):
    """
    Calculate the normalized value using the Min-Max-Normalization.
    1 is "best" and 0 is "worst".

    :return: The normalized value.
    """
    try:
        # Get the permutations ordered to the
        min_value = list(solution_space.permutations.aggregate(Min(attribute)).values())[0]
        max_value = list(solution_space.permutations.aggregate(Max(attribute)).values())[0]

        # If min == max, then this criteria has no influence on the overall decision.
        if min_value == max_value:
            return 0

        # Calculate the normalized value.
        if max_best:
            normalized_value = (getattr(permutation, attribute) - min_value) / (max_value - min_value)
        else:
            normalized_value = (getattr(permutation, attribute) - max_value) / (min_value - max_value)

        return abs(normalized_value)
    except Exception as e:
        logger.error("Could not normalize the given permutation attributes of solution space '{0}'."
                     .format(str(solution_space.pk)), exc_info=True)
        return 0


def rank(solution_space: solution_models.SolutionSpace,
         rank_values: list):
    """
    Sorts all the permutations of the given solution space in accordance to the given list of values.
    The greater the rank_value, the better is the permutation.
    """
    try:
        # Sort the permutation list in dependence of the rank_values.
        # The greater the value, the better is the permutation.
        sorted_permutations = [[val, per] for val, per in sorted(zip(rank_values,
                                                                     list(solution_space.permutations.all())),
                                                                 key=operator.itemgetter(0),
                                                                 reverse=True)]

        i = 1
        """The rank number."""
        previous_value = None
        """The previous ranked value, used for checking, if the comparison value was the same."""
        for ranked_permutation in sorted_permutations:
            value = ranked_permutation[0]
            permutation = ranked_permutation[1]
            # Check if it has the same value (and consequently the same rank).
            if value == previous_value:
                # Write the ranks in dependence of the permutations queryset.
                permutation.rank = i - 1
                permutation.comparison_value = value
                permutation.save()
            # Not the same value. Not so good, as the previous one. Consequently next rank value.
            else:
                # Write the ranks in dependence of the permutations queryset.
                permutation.rank = i
                permutation.comparison_value = value
                permutation.save()
                i += 1

            previous_value = value

    except Exception as e:
        logger.error("Could not rank the given permutation attributes of solution space '{0}'."
                     .format(str(solution_space.pk)), exc_info=True)
