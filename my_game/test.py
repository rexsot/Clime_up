
class Position:
    def __init__(self, x, y):
        self.x, self.y = x, y

ICE_pos = [
    Position(150, 50),
    Position(450, 50),
    Position(750, 50),
    Position(1770, 50)
]

IRON_pos = [
    Position(300, 250),
    Position(1100, 150),
    Position(1500, 250),
    Position(1700, 450)
]


for i in range(0, len(ICE_pos)):
    print(ICE_pos[i].x, ICE_pos[i].y)

print('')

for i in range(0, len(IRON_pos)):
    print(IRON_pos[i].x, IRON_pos[i].y)
