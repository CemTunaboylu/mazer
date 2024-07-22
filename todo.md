https://pypi.org/project/fibheap/


- include diagonal movement in defaults
- make n-dimensional changes
- package format and serialization
- add Wilson, Fractal Tessellation, Cellular Automaton, DFS, Kruskal and Prim for different maze structures i.e short dead-ends or long corridors
- add configuration parameters to change behavior or chose an algorithm# TODO: can use the non-recursive method here with gray codes
    # TODO: make this n-dimensional
    # TODO: hold each position as a generator if dimensions are big?
# TODO: randint(NUM_CELLS_TO_MERGE_IN_ROW(num_rows)) can randomize
# TODO: you may want to make this a generator
# TODO: make this n-dimensional
    assert len(maze_dims) == 2  # TODO: for now, we support 2d only
# TODO: we can compress the maze into an integer
# TODO: mazes are compressed i.e. when thought as a game scene, one coordinate expands into x boxes.
# TODO: ensure to not intervene with the solution i.e. the shortest path solution
# TODO: maybe I can create all the solutions of length of_length, and then put 1s
# TODO: First of all, there should be random obstacles in the maze.
# TODO: Add pre-processors to maze such as how many obstacles there are etc
# TODO: implement an iterator
        # TODO: implement this
    # TODO: assumes that curr and prev positions only differ in 1 dimension
    # TODO: make this more generic to n-dimensional path connect with a vector
        # TODO: I can implement copy-on-write for this to save space
    # TODO: if there are less than shortest manhattan distance or whatever the distance calc. method is
        # TODO: this should not happen but handle it
