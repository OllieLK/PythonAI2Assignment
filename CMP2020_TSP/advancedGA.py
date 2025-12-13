"""
advancedGA.py

An extended Genetic Algorithm for the Travelling Salesperson Problem.
This class inherits from BaselineGA and introduces:
- Roulette wheel selection
- Inversion mutation

These extensions are designed to improve diversity and convergence
while preserving a valid TSP permutation representation.

Modified by: Oliver Lazarus-Keene
"""

import random
import config
from baselineGA import BaselineGA


class AdvancedGA(BaselineGA):
    """
    AdvancedGA extends the BaselineGA by overriding selection and mutation
    operators while reusing fitness calculation, crossover, and population
    management logic.
    """

    # ------------------------------------------------------------------
    # ROULETTE WHEEL SELECTION
    # ------------------------------------------------------------------
    def perform_roulette_selection(self):
        """
        Perform roulette wheel (fitness proportionate) selection.

        Since TSP is a minimisation problem, fitness values are inverted
        so that shorter routes receive a higher probability of selection.

        Returns:
            A single chromosome selected probabilistically based on fitness.
        """

        # Convert fitness values to selection weights
        # Lower fitness (shorter distance) -> higher weight
        epsilon = 1e-6  # prevents division by zero
        weights = [(1 / (f + epsilon)) for f in self.fitnesses]

        total_weight = sum(weights)
        pick = random.uniform(0, total_weight)

        current = 0
        for individual, weight in zip(self.population, weights):
            current += weight
            if current >= pick:
                return individual

        # Fallback (should never occur, but safe)
        return self.population[-1]

    # ------------------------------------------------------------------
    # INVERSION MUTATION
    # ------------------------------------------------------------------
    def perform_mutation(self, individual):
        """
        Perform inversion mutation on a chromosome.

        Inversion mutation selects two random indices and reverses the
        subsequence between them. This preserves permutation validity
        while allowing meaningful structural changes to the tour.

        Args:
            individual: list of City objects representing a TSP tour

        Returns:
            A mutated copy of the individual.
        """

        # If mutation does not occur, return a safe copy
        if random.random() > config.MUTATION_RATE:
            return individual.copy()

        mutant = individual.copy()
        length = len(mutant)

        if length < 2:
            return mutant

        # Select two indices and reverse the subsequence
        i, j = sorted(random.sample(range(length), 2))
        mutant[i:j] = reversed(mutant[i:j])

        return mutant

    # ------------------------------------------------------------------
    # GENERATION PRODUCTION (with new selection method)
    # ------------------------------------------------------------------
    def produce_new_generation(self):
        """
        Create a new generation using:
        - Roulette wheel selection
        - Ordered crossover (inherited)
        - Inversion mutation

        The population is fully replaced each generation.
        """

        new_population = []

        while len(new_population) < config.POPULATION_SIZE:

            # --- Parent selection using roulette wheel ---
            parent1 = self.perform_roulette_selection()
            parent2 = self.perform_roulette_selection()

            # --- Crossover (inherited from BaselineGA) ---
            offspring1, offspring2 = self.perform_crossover(
                parent1.copy(), parent2.copy()
            )

            # --- Inversion mutation ---
            offspring1 = self.perform_mutation(offspring1)
            offspring2 = self.perform_mutation(offspring2)

            # --- Add offspring to population ---
            new_population.append(offspring1)
            if len(new_population) < config.POPULATION_SIZE:
                new_population.append(offspring2)

        # Replace population and recalculate fitness
        self.population = new_population
        self.calculate_fitness_of_population()

        return self.best_individual, self.best_fitness
