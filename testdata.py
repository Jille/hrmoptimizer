program = """-- HUMAN RESOURCE MACHINE PROGRAM --

    JUMP     d
a:
b:
c:
    COPYFROM 0
    OUTBOX
d:
    COPYFROM 5
    COPYTO   0
e:
    INBOX
    JUMPZ    a
    ADD      0
    COPYTO   0
    INBOX
    JUMPZ    b
    ADD      0
    COPYTO   0
    INBOX
    JUMPZ    c
    ADD      0
    COPYTO   0
    JUMP     e
"""

input = [8, 6, 0, 3, -4, 7, 0, 0, 0, 1, -6, 4, 8, -7, 6, 0]
expected = [14, 6, 0, 0, 6]
tiles = 6
initializedTiles = {5: 0}
