import mmh3
import numpy as np

def gen_grid_3d(n=2, current_grid:np.ndarray|None=None):
    """
    Randomly create a polycube of size n
    """

    if current_grid is None:
        
        # 3x3 grid
        current_grid = np.zeros((3, 3, 3), dtype=np.uint8)
        
        # Current point
        current_grid[1][1][1] = 1 # Center

        # Current neighbours
        current_grid[0][1][1] = 2 # Forwards
        current_grid[2][1][1] = 2 # Backwards
        current_grid[1][0][1] = 2 # Top
        current_grid[1][2][1] = 2 # Bottom
        current_grid[1][1][0] = 2 # Left
        current_grid[1][1][2] = 2 # Right

    for i in range(n-1):
        # Select a random neighbour (value=2)
        x_positions, y_positions, z_positions = np.nonzero(current_grid == 2)
        index = np.random.randint(0, len(x_positions))
        x_pos, y_pos, z_pos = x_positions[index], y_positions[index], z_positions[index]

        # Turn selected neighbour into a point
        current_grid[x_pos][y_pos][z_pos] = 1

        # Pad if on border        
        current_grid = np.pad(current_grid,
            (
                (1 if x_pos == 0 else 0, 1 if x_pos == current_grid.shape[0]-1 else 0),
                (1 if y_pos == 0 else 0, 1 if y_pos == current_grid.shape[1]-1 else 0),
                (1 if z_pos == 0 else 0, 1 if z_pos == current_grid.shape[2]-1 else 0)
            )
        )

        # Move our selected point if we padded below it
        x_pos = 1 if x_pos==0 else x_pos
        y_pos = 1 if y_pos==0 else y_pos
        z_pos = 1 if z_pos==0 else z_pos

        # Set nearby points as neighbours
        if not current_grid[x_pos][y_pos][z_pos+1] == 1:
            current_grid[x_pos][y_pos][z_pos+1] = 2
        
        if not current_grid[x_pos][y_pos][z_pos-1] == 1:
            current_grid[x_pos][y_pos][z_pos-1] = 2

        if not current_grid[x_pos][y_pos+1][z_pos] == 1:
            current_grid[x_pos][y_pos+1][z_pos] = 2
        
        if not current_grid[x_pos][y_pos-1][z_pos] == 1:
            current_grid[x_pos][y_pos-1][z_pos] = 2
        
        if not current_grid[x_pos+1][y_pos][z_pos] == 1:
            current_grid[x_pos+1][y_pos][z_pos] = 2
        
        if not current_grid[x_pos-1][y_pos][z_pos] == 1:
            current_grid[x_pos-1][y_pos][z_pos] = 2

    # Return result
    return current_grid

def count_head_zeros(in_):
    count = 0
    for c in in_:
        if c == "0":
            count += 1
        else:
            break
    return count

def harmonic_mean(buckets):
    n = len(buckets)
    scores = [ 1 / i for i in buckets]
    return n / sum(scores)

num_buckets = 16
buckets = [1] * num_buckets

max_iter = 1000000
i = 0
while True:
    i += 1   
    result = bin(int.from_bytes(mmh3.hash_bytes(gen_grid_3d(8)), "big"))[2:].zfill(128)
    score = count_head_zeros(result)

    bucket_idx = int(result[-8:], 2) % num_buckets

    if score > buckets[bucket_idx]:
        buckets[bucket_idx] = score
        print(score)
    
    if i % 10000 == 0:
        print(f"{i*100/max_iter:.2f}% Current Score: {2**harmonic_mean(buckets)}")
    
    if i == max_iter:
        break
