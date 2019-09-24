# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.
import random


class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y

    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"

    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)

    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0

    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1  # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west
        horDirction = 1  # 1: up, -1: down

        # Generated Room Names
        roomAdj = ["Dark", "Old", "Old, Intact", "Loathsome", "Horrid",
                   "Empty", "Moist, Murky", "Suspicous", "Damp", "Gloomy", "Secret", "Filthy", "Misty", "Moldy", "Pestilent", "Cozy Little", "Dim", "Smokey", "Vacant", "Ancient"]
        roomNames = ["Cellar", "Cave", "Cabin", "Hideout",
                     "Pathway", "Corridor", "Cave", "Hideout",
                     "Pathway", "Corridor", "Treasure Room"]

        # Generated Room Descriptions
        descStarters = [
            "You approach a(n)", "You step forward and see a(n)", "You walk into a(n)", "This is a", "You creep into a(n)"]
        descInfo = ["It seems to give off an errie mood", "Its a pretty dark room, better watch you step!", "You see a sparkling light deeper in the dungeon, is it your imagination?",
                    "A terrible smell creeps up your nose.", "Seems like a cozy place", "Its a very quiet room. Too quiet.", "Its very dark in here.", "Dont be fooled.", "You hear some rocks hit the ground, better watch your step."]
        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:
            # Calculate the direction of the room to be created
            nextDi = random.randint(0, 18)
            canDown = horDirction <= 0
            canUp = horDirction >= 0

            if nextDi > 11 and canDown and not self.grid[y-1][x] and y > 1 and x < size_x - 2 and x > 1:
                room_direction = "s"
                horDirction = -1
                y -= 1
            elif x > 1 and nextDi > 16 and canUp:
                room_direction = "n"
                horDirction = 1
                y += 1
            elif direction > 0 and x < size_x - 1 and not self.grid[y][x+1]:
                room_direction = "e"
                horDirction = 0

                x += 1
            elif direction < 0 and x > 0 and not self.grid[y][x-1]:
                horDirction = 0
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                # If theres a room above it, go to the room above that
                if self.grid[y+1][x]:
                    while self.grid[y+1][x]:
                        y += 1
                        previous_room = self.grid[y][x]
                y += 1
                room_direction = "n"
                horDirction = 1
                direction *= -1

            currName = random.choice(roomAdj) + " " + random.choice(roomNames)
            roomDescription = random.choice(
                descStarters) + " " + currName.lower() + ". " + random.choice(descInfo)

            # print(horDirction)
            # Create a room in the given direction
            room = Room(room_count, currName,
                        roomDescription, x, y)
            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            self.grid[y][x] = room
            # print(self.grid[y][x].description)

            # Connect the new room to the previous room
            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)
            if nextDi < 10 and y > 0 and self.grid[y-1][x]:
                room.connect_rooms(self.grid[y-1][x], "s")
            # elif nextDi < 5 and self.grid[y][x+1]:
            #     room.connect_rooms(self.grid[y][x+1], "e")
            # Update iteration variables
            previous_room = room
            room_count += 1

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''
        # print(self.grid[0][0].name, self.grid[0][0].description)
        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
num_rooms = 115
width = 15
height = 15
w.generate_rooms(width, height, num_rooms)
w.print_rooms()

print(w.grid[0][10])
print(
    f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
