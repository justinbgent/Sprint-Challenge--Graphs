from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
#map_file = "maps/main_maze.txt"

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
    old_room = None
    traveled = {}
    traveled[current_room.id] = set()

    # set initial direction to the first exit in the list
    exits = current_room.get_exits()
    direction = exits[0]

    path = []

    while len(traveled) < room_count:
        # travel
        old_room = current_room
        current_room = current_room.get_room_in_direction(direction)
        path.append(direction)
        if current_room.id not in traveled:
            traveled[current_room.id] = set()
        traveled[old_room.id].add(direction)
        # choose next direction
        exits = current_room.get_exits()
        if len(exits) > 1:
            past_choices = traveled[current_room.id]
            for choice in exits:
                if not past_choices.__contains__(choice):
                    direction = choice
        else:
            direction = exits[0]

    return path

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
