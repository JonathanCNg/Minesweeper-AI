# Minesweeper-AI

An AI to play the classic game, Minesweeper. ([Play Minesweeper](https://minesweeperonline.com/#intermediate))

## Demo

<img src="README Files/Minesweeper AI Demo.gif" height="300"/>

## Tools Used
1. Python (https://www.python.org/)

## Final AI Report

### I.A Briefly describe your Minimal AI algorithm. What did you do that was fun, clever, or creative?

<img src="README Files/1_effective-label.png" width="200"/>

The first step for the AI was to create a “Rule of Thumb” algorithm that could determine the safe and mine tiles simply by analyzing a single uncovered tile and its neighbors. Label is 0? Unflag all neighbors. Effective label equal to the quantity of covered neighbors? The covered neighbors must be mines to flag. The tile label equals its quantity of flagged neighbors? Its covered, unflagged neighbors must be safe.

Of course, this algorithm by itself is narrowminded and doesn’t include inferring safe and mine tiles based on the conditions of its neighbors. Logical inference came at a later stage in development. More importantly, it fails to complete a game in most circumstances. Thus, in order to continue making moves where “Rule of Thumb” fails, we created a guessing algorithm that uncovers a neighbor of the “Least Risk Tile”.

The equation for calculating risk:

<img src="README Files/2_risk.png" width="200"/>

### I.B Describe your Minimal AI algorithm's performance:

<img src="README Files/3_chart.png" height="200"/>

Minimal AI surpassed our expectations, solving all of Easy and the majority of Beginner, and Intermediate worlds. Minimal AI struggled with Expert worlds with only a 3.9% win percentage. Overall, a minority (40.1%) of the worlds were won.

### II.A. Briefly describe your Final AI algorithm, focusing mainly on the changes since Minimal AI:

We added a “Subset Neighbor” algorithm. If an uncovered tile, TileA, has covered neighbors which are a superset of the covered neighbors of a second uncovered tile, TileB, we check: If the TileA/TileB effective value difference is 0, TileA’s exclusive covered neighbors are not mines and shall be uncovered. If the TileA/TileB effective value difference is equal to the difference of covered neighbors, TileA’s exclusive covered neighbors are mines to be flagged.

<img src="README Files/4-5_heuristic.png" height="300"/>

We also implemented an algorithm similar to “Subset Neighbor” which considers TileC and TileD, which have intersecting covered neighbors and one exclusive coveredneighbor. If Tile C has an effective label which is 1 greater than the effective label of Tile D, Tile B’s exclusive covered neighbor is not a mine and can be uncovered.

We also implemented a DFS to explore all the valid mine combinations on the frontier. If a tile was unflagged in all valid mine combinations, the tile could be safely uncovered. If a tile was flagged in all valid mine combinations, it was a mine to be flagged. While it is functional, it remains ineffecient. As such, we have commented it out in our final submission.

### II.B Describe your Final AI algorithm's performance:

<img src="README Files/6_chart.png" height="200"/>

Final AI is a significant improvement with over 150% of the performance of Minimal AI, when looking at overall worlds solved. While all measures improved, Expert worlds improved the most with Final AI performing at over 700% of Minimal AI. With Minimal AI, a minority of the worlds were won. With Final AI, a majority of the worlds were won!
