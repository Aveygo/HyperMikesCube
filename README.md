# Hyper Mikes Cube
https://www.youtube.com/watch?v=g9n0a0644B4

Given a number of cubes, how many ways could you uniquely arrange them? 

## The algorithm
1. After generating an arrangment of cubes, we will compute it's hash.
2. The number of consequative zeros at the start of the hash is the score.
3. The last 8 bits mod num_buckets is the bucket to choose from.
4. If the score is larger than the selected bucket's score, replace it.
5. Repeat...
6. Profit???
7. Estimated arrangements = 2 ^ harmonic mean of buckets.

This results in a probabilistic method (which *is* suboptimal) of finding the number of cubes, **but** comes with far less coding, complexity, easy multithreading/scaling, and imo is "good enough" to at least get an estimate for larger numbers of cubes.

## Caveats
1. Rotation and flipping is not accounted for.
2. It still takes quite a bit of computation.
3. I have a potato as a PC.
4. Have no idea when it converges (if it does?)
5. Zero regard for multithreading, etc, just an experiment.

## Results
todo
