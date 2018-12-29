program = """-- HUMAN RESOURCE MACHINE PROGRAM --

a:
    COPYFROM 5
    COPYTO   0
b:
    INBOX   
    JUMPZ    c
    ADD      0
    COPYTO   0
    INBOX   
    JUMPZ    d
    ADD      0
    COPYTO   0
    INBOX   
    JUMPZ    e
    ADD      0
    COPYTO   0
    JUMP     b
c:
d:
e:
    COPYFROM 0
    OUTBOX  
    JUMP     a
"""

input = [8, 6, 0, 3, -4, 7, 0, 0, 0, 1, -6, 4, 8, -7, 6, 0]
expected = [14, 6, 0, 0, 6]
tiles = 6
initializedTiles = {5: 0}
