from room import Room
from player import Player
from world import World


# Note: This Queue class is sub-optimal. Why?
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)#because it is removing elements from the from of array. doubly linked list would be better suited
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


import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = ['n', 'n', 's', 's', 's', 's', 'n', 'n', 'w', 'w', 'e', 'e', 'e', 'e']

def build_traversal_path(starting_room, room_count):
    current_room = starting_room
    traveled = set()
    traveled.add(current_room.id)

    # set initial direction to the first exit in the list
    exits = current_room.get_exits()

    final_path = []
    path = []
    stack = Stack()
    for exit in exits:
        stack.push(current_room.get_room_in_direction(exit))

    while len(traveled) < room_count:
        destination_room = stack.pop()

        # do bfs that will return path to destination
        q = Queue()
        for exit in exits:
            q.enqueue([exit])
        bfs_room = current_room
        visited = set() #[set(), bfs_room]
        while q.size() > 0:
            path = q.dequeue()
            bfs_room = current_room
            for exit in path:
                bfs_room = bfs_room.get_room_in_direction(exit)
            bfs_exits = bfs_room.get_exits()
            if bfs_room.id not in visited:
                visited.add(bfs_room.id)
                if bfs_room == destination_room:
                    break
                for exit in bfs_exits:
                    #could add some rule to make it not add the backwards path to the queue or add 
                    # the opposite direction to the queue. If the room only has the opposite direction
                    # then simply don't add this path to the queue
                    # for now I will keep the backwards paths as part of the queue
                    new_path = list(path)
                    new_path.append(exit)
                    q.enqueue(new_path)

        # travel path (be sure to append directions to the final_path)
        for exit in path:
            current_room = current_room.get_room_in_direction(exit)
            final_path.append(exit)
        
        # now mark the room as traveled
        if current_room.id not in traveled:
            traveled.add(current_room.id)

        # add newly discovered rooms to stack
        exits = current_room.get_exits()
        for exit in exits:
            room = current_room.get_room_in_direction(exit)
            if room.id not in traveled:
                stack.push(room)


        #exits = current_room.get_exits()
        #if len(exits) > 1:
        #    past_choices = traveled[current_room.id]
        #    for choice in exits:
        #        if not past_choices.__contains__(choice):
        #            direction = choice
        #else:
        #    direction = exits[0]

    return final_path

traversal_path = build_traversal_path(world.starting_room, len(room_graph))

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
#player.current_room.print_room_description(player)
#while True:
#    cmds = input("-> ").lower().split(" ")
#    if cmds[0] in ["n", "s", "e", "w"]:
#        player.travel(cmds[0], True)
#    elif cmds[0] == "q":
#        break
#    else:
#        print("I did not understand that command.")
