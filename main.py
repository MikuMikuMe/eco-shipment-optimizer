To create an `eco-shipment-optimizer` for optimizing delivery routes and load planning to minimize carbon emissions and reduce costs, we need to consider the following:

1. **Input Data**: The tool requires input data, which typically includes vehicle capacities, available routes, distance information, and possibly carbon emission factors for different vehicle types.

2. **Optimization Goal**: Minimize carbon emissions and costs. This typically involves finding the shortest or most fuel-efficient routes and optimizing the load distribution among available vehicles.

3. **Tools and Libraries**: Python has several libraries that can help with optimization, including `networkx` for graph-based route optimization and `numpy` for numerical calculations. For routing problems, `ortools` (Google's Optimization Tools) can be useful.

Below is a simple version of an eco-shipment-optimizer. This version focuses on using Dijkstra's algorithm to find the shortest path while considering carbon emissions and also includes load optimization. Note that this is a simplified approach; real-world logistics optimization can be much more complex.

```python
import networkx as nx
import numpy as np

class EcoShipmentOptimizer:
    def __init__(self):
        # Initialize a directed graph
        self.graph = nx.DiGraph()
    
    def add_route(self, source, target, distance, emission_factor, cost):
        """
        Add route information to the graph.
        source: starting point
        target: destination point
        distance: distance between source and target
        emission_factor: carbon emission per unit distance for this route
        cost: transportation cost per unit distance for this route
        """
        self.graph.add_edge(source, target, distance=distance, emission=emission_factor * distance, cost=cost * distance)

    def calculate_min_emission_path(self, source, target):
        """
        Returns the route with the minimum carbon emissions.
        """
        try:
            # Get the shortest path based on emission
            path = nx.shortest_path(self.graph, source, target, weight='emission')
            emission = nx.shortest_path_length(self.graph, source, target, weight='emission')
            return path, emission
        except nx.NetworkXNoPath:
            return [], float('inf')

    def calculate_min_cost_path(self, source, target):
        """
        Returns the route with the minimum cost.
        """
        try:
            # Get the shortest path based on cost
            path = nx.shortest_path(self.graph, source, target, weight='cost')
            cost = nx.shortest_path_length(self.graph, source, target, weight='cost')
            return path, cost
        except nx.NetworkXNoPath:
            return [], float('inf')

    def optimize_load(self, demands, vehicle_capacity):
        """
        Optimize the load distribution among vehicles.
        demands: list of demands (load requirements) by customers
        vehicle_capacity: maximum load a vehicle can carry
        """
        demands = sorted(demands, reverse=True)
        load_plans = []
        current_vehicle_load = []

        for demand in demands:
            if sum(current_vehicle_load) + demand <= vehicle_capacity:
                current_vehicle_load.append(demand)
            else:
                load_plans.append(current_vehicle_load)
                current_vehicle_load = [demand]

        if current_vehicle_load:
            load_plans.append(current_vehicle_load)

        return load_plans

# Main function to demonstrate the usage
def main():
    optimizer = EcoShipmentOptimizer()
    
    # Adding some hypothetical routes (source, target, distance, emission_factor(g/m), cost($/m))
    optimizer.add_route("A", "B", 100, 0.1, 1.0)
    optimizer.add_route("B", "C", 50, 0.2, 0.5)
    optimizer.add_route("A", "C", 140, 0.15, 0.85)
    optimizer.add_route("C", "D", 60, 0.18, 0.9)
    
    # Optimize routes
    min_emission_path, min_emission = optimizer.calculate_min_emission_path("A", "D")
    min_cost_path, min_cost = optimizer.calculate_min_cost_path("A", "D")
    
    print(f"Minimum Emission Path: {min_emission_path}, Emission: {min_emission}")
    print(f"Minimum Cost Path: {min_cost_path}, Cost: {min_cost}")

    # Optimize load distribution
    demands = [30, 40, 20, 50, 30]
    vehicle_capacity = 100
    load_plans = optimizer.optimize_load(demands, vehicle_capacity)
    
    print(f"Load Plans: {load_plans}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
```

### Comments:
- The **graph** represents the network of routes, with **nodes** as locations and **edges** as routes with associated distances, emission factors, and costs.
- **Dijkstra’s Algorithm** is employed for calculating the shortest paths based on emissions or costs using NetworkX's built-in functionality.
- `optimize_load` function distributes loads efficiently among available vehicles based on their capacity.
- Basic error handling is included in the main function to catch exceptions and ensure that the program does not crash unexpectedly.

### Considerations:
- This example is highly simplified and doesn't take into account dynamic factors such as traffic, real-time fuel prices, or delivery time constraints. 
- In practice, integration with GPS and real-time data sources might also be required for more precise optimization.