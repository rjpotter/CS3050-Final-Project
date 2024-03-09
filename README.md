# CS3050-Final-Project

## Description
The game Stratego. Stratego is a classic board game of battlefield strategy that combines elements of stealth, tactics, and surprise. Designed for two players, the game represents a battle between two armies, with the objective of capturing the opponent's flag or eliminating their ability to move. Each player controls 40 pieces representing individual officer and soldier ranks in an army, with each piece's rank hidden from the opponent. Pieces have varying ranks and powers, and the setup is secret at the start of the game. Players move their pieces across a board, with the goal of attacking the opponent’s pieces to discover their rank and capture the flag. The catch is that lower-ranked pieces can defeat higher ranks in specific scenarios, adding a layer of strategic depth and bluffing.

## Rules
- **Setup**: Each player places their 40 pieces on their side of the 10x10 board, hiding the ranks from their opponent. The arrangement can vary, but pieces must be placed in the four rows closest to the player.
- **Objective**: Capture the opponent's flag or trap all of their movable pieces so they cannot make a move.
- **Movement**: Players take turns moving one piece per turn. Pieces can move one square horizontally or vertically (not diagonally), except for the Scout, which can move any distance in a straight line.
- **Attacks**: To attack, move your piece into a square occupied by an opposing piece. Both players then reveal their ranks; the lower-ranked piece is removed from the board. If the ranks are equal, both pieces are removed.
- **Special Pieces**:
  - The Flag is immobile and must be protected.
  - Bombs destroy any attacking piece except Miners.
  - Miners can defuse Bombs, removing them without being destroyed.
  - The Spy can defeat the highest-ranking piece, the Marshal, if the Spy attacks.
- **No Entry Zones**: Two "lakes" in the center of the board are impassable and pieces cannot move through or onto these squares.
- **Winning**: The game ends when one player captures the opponent's flag or the opponent cannot make any legal moves.
- **Prohibited Moves**: Pieces cannot move back and forth between the same two squares repeatedly (two-square rule) to avoid indefinite continuation of the game.

## Sprint 1 Goals

### Task Priorities and Details

1. **Initialize Board**
   - **Priority**: Essential
   - **Difficulty**: Easy
   - **Notes**: Each player will have a pre-set starting position.
   - **Status**: Completed. The board is initialized with troops in their starting positions for both human and computer players.

2. **Cell Type Enum**
   - **Priority**: Essential
   - **Difficulty**: Easy
   - **Notes**: Define enum types for different cell states or contents.
   - **Status**: Completed. The `Cell` enum classifies all possible cell types, including troops, bombs, and the flag.

3. **Computer that Can Move Pieces (basic)**
   - **Priority**: Important
   - **Difficulty**: Medium
   - **Notes**: Moves can be mostly random, scouts will not be able to do non-standard moves.
   - **Status**: In Progress. Basic infrastructure for move generation is in place, though specific logic for moves, including scouts, is pending.

4. **Learn PyArcade**
   - **Priority**: Important
   - **Difficulty**: Medium
   - **Notes**: Successful if we can get a window with a single graphic.
   - **Status**: In Progress. We have successfully built the framework and initialized a window. 

5. **List of Edge Cases**
   - **Priority**: Nice to have
   - **Difficulty**: Medium
   - **Notes**: Get the list of all the comparisons for every situation (water, troop comparisons like Spy->Marshal, etc.).
   - **Status**: In Progress. Basic comparisons and some edge cases have been implemented, with more complex scenarios to follow.

6. **Game End Detection**
   - **Priority**: Nice to have
   - **Difficulty**: Easy
   - **Notes**: Just detecting if a troop captures the enemy flag.
   - **Status**: Completed. Game can detect the capture of the flag.

7. **Troop Type Comparison**
   - **Priority**: Nice to have
   - **Difficulty**: Easy
   - **Notes**: Basically deciding who wins based on a troop attacking another.
   - **Status**: Completed for basic cases. Additional logic for more complex troop interactions is in development.

## Date
3/4/2024
