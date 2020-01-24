from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk

traversal_path = []
traversal_graph = {0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}}

# Create a stack that has rooms to go to incase of dead end
good_rooms = Stack()



opp_dir = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e',
}

def get_paths(room_id):
    paths = []
    for direction, room in traversal_graph[room_id].items():
        if room == '?':
            paths.append(direction)

    return paths

def isFilled():
    filled = True
    for i in traversal_graph.values():
        if '?' in i.values():
            filled = False
    return filled

def bfs(starting_room, destination_room):
        """
        Return a list of direction to follow to get from
        starting room to destination room
        """
        queue = Queue()

        visited = set()
        
        queue.enqueue([starting_room])

        while queue.size() > 0:

            path = queue.dequeue()

            room = path[-1]

            if room not in visited:

                if room == destination_room:
                    break

                visited.add(room)

                for next_room in list(traversal_graph[room].values()):
                    if next_room != '?':
                        new_path = list(path)
                        new_path.append(next_room)
                        queue.enqueue(new_path)

        # Convert path to directions
        directions = []
        for i in range(len(path) - 1):
            for direction, room in traversal_graph[path[i]].items():
                if room == path[i+1]:
                    directions.append(direction)
        
        return directions

while isFilled() == False:
    # Assign current room to variable
    current_room = player.current_room.id
    
    # Push room to good rooms
    if len(get_paths(current_room)) > 1:
        good_rooms.push(current_room)

    # Get available paths that are not searched
    available_paths = get_paths(current_room)
    
    # If no available paths
    if not available_paths:
        # Find shortest path to a good room

        found_room = False
        while found_room == False:
            backup_room = good_rooms.pop()
            if len(get_paths(backup_room)) > 0:
                found_room = True
        move_back = bfs(current_room, backup_room)

        # Travel to it
        for move in move_back:
            player.travel(move)

        # Add travel to traversal path
        traversal_path += move_back

        # Make room traveled to the current room
        current_room = player.current_room.id

        # Get available paths from room
        available_paths = get_paths(current_room)

        # If room still has enough paths, add back to good rooms
        if len(get_paths(current_room)) > 1:
            good_rooms.push(current_room)

    connected_exits = {}
    # Assign directions with the amount of exits in the rooms
    if 's' in available_paths:
        temp_direction = 's'
        player.travel(temp_direction)
        connected_exits[temp_direction] = len(player.current_room.get_exits())
        player.travel(opp_dir[temp_direction])
    if 'w' in available_paths:
        temp_direction = 'w'
        player.travel(temp_direction)
        connected_exits[temp_direction] = len(player.current_room.get_exits())
        player.travel(opp_dir[temp_direction])
    if 'n' in available_paths:
        temp_direction = 'n'
        player.travel(temp_direction)
        connected_exits[temp_direction] = len(player.current_room.get_exits())
        player.travel(opp_dir[temp_direction])
    if 'e' in available_paths:
        temp_direction = 'e'
        player.travel(temp_direction)
        connected_exits[temp_direction] = len(player.current_room.get_exits())
        player.travel(opp_dir[temp_direction])

    # If there are more than 1 conne
    if len(connected_exits) > 1 and 1 in connected_exits.values():
        min_direction = ''
        min_exits = 10
        for direction, exits in connected_exits.items():
            if exits < min_exits:
                min_direction = direction
                min_exits = exits

        direction = min_direction
    else:
        if 's' in available_paths:
            direction = 's'
        elif 'w' in available_paths:
            direction = 'w'
        elif 'n' in available_paths:
            direction = 'n'
        elif 'e' in available_paths:
            direction = 'e'
    
    # Make player travel in direction
    player.travel(direction)

    # Add travel direction to the traversal_path
    traversal_path.append(direction)
    
    # If room not in graph create room
    if player.current_room.id not in traversal_graph:
        traversal_graph[player.current_room.id] = {i : '?' for i in player.current_room.get_exits()}

    # Add the rooms to the directions in the graph
    traversal_graph[current_room][direction] = player.current_room.id
    traversal_graph[player.current_room.id][opp_dir[direction]] = current_room
    





# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
