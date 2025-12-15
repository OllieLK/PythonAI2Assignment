"""
advancedGA.py

Advanced Genetic Algorithm for the Travelling Salesperson Problem.

Extensions beyond the baseline GA:
- Roulette wheel (fitness-proportionate) selection
- Inversion mutation
- Walls-aware fitness using BFS shortest paths
- Cached city-to-city path distances for efficiency
- Improved stopping condition using convergence (stagnation)

Modified by: Oliver Lazarus-Keene
"""

import random
from collections import deque

import config
from baselineGA import BaselineGA


class AdvancedGA(BaselineGA):
    """
    AdvancedGA extends BaselineGA by modifying selection, mutation,
    fitness evaluation, and stopping criteria, while reusing the
    baseline representation and crossover operator.
    """

    def __init__(self, world):
        super().__init__(world)

        # Cache for shortest path lengths between city pairs
        # Key: (city_name_A, city_name_B) -> int steps or None if unreachable
        self._path_cache = {}

        # Convergence tracking
        self._last_best_fitness = None
        self._stall_count = 0

    # ------------------------------------------------------------------
    # Roulette Wheel Selection
    # ------------------------------------------------------------------
    def perform_roulette_selection(self):
        """
        Roulette wheel (fitness-proportionate) selection.

        As TSP is a minimisation problem, fitness values are inverted
        so that lower fitness values have higher selection probability.

        Returns:
            One selected chromosome.
        """
        epsilon = 1e-9

        weights = []
        for f in self.fitnesses:
            if f is None or f < 0:
                weights.append(0.0)
            else:
                weights.append(1.0 / (f + epsilon))

        total_weight = sum(weights)

        # Fallback to uniform random selection if all weights are zero
        if total_weight <= 0.0:
            return random.choice(self.population)

        pick = random.uniform(0.0, total_weight)
        current = 0.0

        for individual, weight in zip(self.population, weights):
            current += weight
            if current >= pick:
                return individual

        return self.population[-1]  # safety fallback

    # ------------------------------------------------------------------
    # Inversion Mutation
    # ------------------------------------------------------------------
    def perform_mutation(self, individual):
        """
        Inversion mutation.

        With probability MUTATION_RATE, selects two indices i < j and
        reverses the subsequence individual[i:j].

        Returns:
            A (possibly mutated) copy of the chromosome.
        """
        mutant = individual.copy()

        if random.random() > config.MUTATION_RATE:
            return mutant

        length = len(mutant)
        if length < 2:
            return mutant

        i, j = sorted(random.sample(range(length), 2))
        mutant[i:j] = reversed(mutant[i:j])

        return mutant

    # ------------------------------------------------------------------
    # BFS shortest path (walls-aware)
    # ------------------------------------------------------------------
    def _bfs_shortest_path_length(self, start_pose, goal_pose):
        """
        Computes the shortest number of valid moves between two poses
        using BFS, expanding only actions returned by world.get_actions(),
        thereby respecting walls and boundaries.

        Returns:
            int path length if reachable, otherwise None.
        """
        if start_pose.x == goal_pose.x and start_pose.y == goal_pose.y:
            return 0

        queue = deque()
        queue.append((start_pose, 0))

        visited = set()
        visited.add((start_pose.x, start_pose.y))

        while queue:
            current_pose, dist = queue.popleft()

            # Expand only legal actions (respects walls)
            for next_pose in self.world.get_actions(current_pose):
                key = (next_pose.x, next_pose.y)

                if key in visited:
                    continue

                if next_pose.x == goal_pose.x and next_pose.y == goal_pose.y:
                    return dist + 1

                visited.add(key)
                queue.append((next_pose, dist + 1))

        return None  # unreachable

    def _path_cost_between_cities(self, city_a, city_b):
        """
        Returns cached shortest-path cost between two cities.
        """
        key = (city_a.name, city_b.name)
        if key in self._path_cache:
            return self._path_cache[key]

        cost = self._bfs_shortest_path_length(city_a.pose, city_b.pose)

        # Cache both directions (symmetric)
        self._path_cache[(city_a.name, city_b.name)] = cost
        self._path_cache[(city_b.name, city_a.name)] = cost

        return cost

    # ------------------------------------------------------------------
    # Fitness Calculation (walls-aware)
    # ------------------------------------------------------------------
    def calculate_fitness(self, chromosome):
        """
        Calculates fitness as the sum of shortest traversable path lengths
        between consecutive cities (including return to start).
        """
        cities = self.convert_chromosome_to_city_list(chromosome)
        n = len(cities)

        if n < 2:
            return 0.0

        total_cost = 0.0

        for i in range(n):
            city_a = cities[i]
            city_b = cities[(i + 1) % n]

            cost = self._path_cost_between_cities(city_a, city_b)

            if cost is None:
                return config.UNREACHABLE_PENALTY

            total_cost += cost

        return total_cost

    # ------------------------------------------------------------------
    # Generation Production
    # ------------------------------------------------------------------
    def produce_new_generation(self):
        """
        Produces a new generation using:
        - Roulette wheel selection
        - Ordered one-point crossover (inherited)
        - Inversion mutation
        """
        new_population = []

        while len(new_population) < config.POPULATION_SIZE:
            parent1 = self.perform_roulette_selection()
            parent2 = self.perform_roulette_selection()

            child1, child2 = self.perform_crossover(
                parent1.copy(), parent2.copy()
            )

            child1 = self.perform_mutation(child1)
            child2 = self.perform_mutation(child2)

            new_population.append(child1)
            if len(new_population) < config.POPULATION_SIZE:
                new_population.append(child2)

        self.population = new_population
        self.calculate_fitness_of_population()

        return self.best_individual, self.best_fitness

    # ------------------------------------------------------------------
    # Improved Stopping Condition
    # ------------------------------------------------------------------
    def finished(self):
        """
        Stops the GA when either:
        - MAX_NUMBER_OF_GENERATIONS is reached, OR
        - Best fitness has not improved for STALL_LIMIT generations.
        """

        if self.number_of_generations >= config.MAX_NUMBER_OF_GENERATIONS:
            return True

        if self._last_best_fitness is None:
            self._last_best_fitness = self.best_fitness
            return False

        if self.best_fitness < self._last_best_fitness:
            self._last_best_fitness = self.best_fitness
            self._stall_count = 0
        else:
            self._stall_count += 1

        return self._stall_count >= config.STALL_LIMIT
