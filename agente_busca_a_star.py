import heapq

class Node:
    def __init__(self, city, parent=None, g=0, h=0):
        self.city = city
        self.parent = parent
        self.g = g
        self.h = h

    def get_f_cost(self):
        return self.g + self.h

    def __lt__(self, other):
        return self.get_f_cost() < other.get_f_cost()

def a_star_search(graph, start_city, goal_city, heuristic):
    open_list = []
    closed_set = set()

    start_node = Node(city=start_city, parent=None, g=0, h=heuristic.get(start_city, 0))
    heapq.heappush(open_list, (start_node.get_f_cost(), start_node))
    open_list_nodes = {start_city: start_node}

    while open_list:
        _, current_node = heapq.heappop(open_list)
        
        if current_node.city in closed_set:
            continue
        closed_set.add(current_node.city)
        
        if current_node.city == goal_city:
            path = []
            cost = current_node.g
            temp = current_node
            while temp is not None:
                path.append(temp.city)
                temp = temp.parent
            return path[::-1], cost

        for neighbor_city, cost_to_neighbor in graph.get(current_node.city, []):
            if neighbor_city in closed_set:
                continue
            
            tentative_g = current_node.g + cost_to_neighbor
            neighbor_node = open_list_nodes.get(neighbor_city)

            if neighbor_node is None or tentative_g < neighbor_node.g:
                new_h = heuristic.get(neighbor_city, 0)
                new_neighbor_node = Node(city=neighbor_city, parent=current_node, g=tentative_g, h=new_h)
                heapq.heappush(open_list, (new_neighbor_node.get_f_cost(), new_neighbor_node))
                open_list_nodes[neighbor_city] = new_neighbor_node
                
    return None, None

def main():
    print("Agente Inteligente para Busca de Rota com A* ")

    graph = {
        'Belo Horizonte': [('Juiz de Fora', 285), ('Varginha', 320)],
        'Juiz de Fora': [('Belo Horizonte', 285), ('Rio de Janeiro', 185)],
        'Varginha': [('Belo Horizonte', 320), ('Campinas', 300)],
        'Rio de Janeiro': [('Juiz de Fora', 185), ('Sao Paulo', 435)],
        'Campinas': [('Varginha', 300), ('Sao Paulo', 95)],
        'Sao Paulo': [('Rio de Janeiro', 435), ('Campinas', 95)]
    }

    heuristic = {
        'Belo Horizonte': 500,
        'Juiz de Fora': 370,
        'Varginha': 270,
        'Rio de Janeiro': 360,
        'Campinas': 90,
        'Sao Paulo': 0
    }

    start_city = 'Belo Horizonte'
    goal_city = 'Sao Paulo'

    print(f"\nBuscando o caminho de '{start_city}' para '{goal_city}'...")

    path, cost = a_star_search(graph, start_city, goal_city, heuristic)

    if path:
        print("\n✅ Busca concluída com sucesso!")
        print(f"   Caminho encontrado: {' -> '.join(path)}")
        print(f"   Custo total do caminho: {cost} km")
    else:
        print(f"\n❌ Não foi possível encontrar um caminho de '{start_city}' para '{goal_city}'.")

if __name__ == "__main__":
    main()