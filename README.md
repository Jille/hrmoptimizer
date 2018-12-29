# Human Resource Machine optimizer

https://tomorrowcorporation.com/humanresourcemachine

A toy project that optimizes code written for the Human Resource Machine.

Programs are first parsed by `parser.py` into a "program": a list of instructions and labels.

Jumps are then factored out by `blocks.py` into a DCG (Directed Cyclic Graph) of blocks. Each block has a defaultDestination and a conditionalDestination (for JUMPZ and JUMPN). Each block has a list of 0 or more instructions, none of them jumps.

Block DSGs are executed by `runner.py` to find out what the hot blocks are so we know what to optimize for.

Last, `stringer.py` turns the DSG of blocks back into a HRM program.
