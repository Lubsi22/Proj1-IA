# Water Sort Puzzle - AI Project

A puzzle-solving game implementation using Artificial Intelligence techniques to automatically solve the classic Water Sort Puzzle challenge. This project combines game development with search algorithms to find optimal solutions for tile-matching puzzles.

---

## (1) Problem Specification

### Definition
Water Sort Puzzle is an interactive puzzle game where players must sort colored water into test tubes to solve a challenging tile-matching problem. The game provides a visual and interactive environment where the objective is to arrange tubes so that each contains water of only a single color.

### Game Rules
- **Tubes**: The game uses multiple test tubes, each with a capacity of 3 or more water layers
- **Pouring Constraint**: Water can only be poured from one tube to another if:
  - The destination tube has available space
  - At least one complete color layer is being transferred
- **Final State**: A puzzle is solved when every tube contains water of only one color, or is completely empty

### Problem Characteristics
- Puzzles can have millions of possible configurations
- Different sequences of moves can lead to the same goal state
- Difficulty increases with tube count, color variety, and initial scramble degree

---

## (2) Related Work

### References and Sources

- **Water Sort Puzzle**: https://play.google.com/store/apps/details?id=com.gma.water.sort.puzzle


---

## (3) Problem Formulation as a Search Problem

### State Representation
A **state** is defined as a configuration of all tubes in the game:
```
state = [Bottle₁, Bottle₂, ..., Bottleₙ]
```
Each Bottle object contains:
- `colors`: An ordered list of color strings representing water layers (bottom to top)
- Example state: `[['red','red','blue'], ['red','blue','blue'], []]` - 3 tubes with mixed colors

### Initial State
A randomly configured puzzle where:
- Colors are distributed across multiple tubes
- Each tube may contain multiple different colors
- No tube contains only a single color (except possibly empty tubes)

### Goal State
A **solved** state where:
- Every non-empty tube contains exactly one color (all layers are identical) or the tube is completely empty
- Example goal state: `[['red','red','red'], ['blue','blue','blue'], []]`

### Operators (Actions)
**Pour(source_tube, destination_tube)**
- Transfers water color(s) from source to destination
- **Preconditions**:
  - `source_tube.colors` is not empty 
  - `len(destination_tube.colors) < max_len` (has space) OR `destination_tube.colors` is empty 
- **Effect**: Pops consecutive same color layers from source, appends to destination
- **Cost**: 1 move

### Heuristic Functions (for informed search)


---

## (4) Implementation Carried Out

### Technology Stack
- **Language**: Python 
- **Graphics Engine**: Pygame
- **Architecture Pattern**: Model-View-Controller (MVC)

### System Architecture

#### Model Layer (`src/Model/Bottle.py`)
- **Bottle Class**: Represents a single test tube
  - **Attributes**:
    - `colors`: List of strings (e.g., `['red', 'blue', 'red']`)
    - `cords`: Tuple of 4 corner coordinates `[(x₀,y₀), (x₁,y₁), (x₂,y₂), (x₃,y₃)]` for rendering
    - `x, y, width, height`: Derived spatial properties for collision detection
  - **Methods**:
    - `check_color()`: Boolean validation - returns True if tube is solved (monochromatic or empty)

#### Controller Layer (`src/Controller/`)
- **Controller.py - Game Logic**
  - `select_bottle(mouse_pos, bottles)`: Mouse click handler for tube selection
    - Detects collision between cursor and tube boundaries
    - Manages pour operation between selected tubes
  - `pour(source, destination)`: Core game mechanic
    - Validates pour constraints programmatically
    - Transfers color layer from source to destination
    - Returns True on success, False on invalid move
  - `check_win(bottles)`: Goal state validator
    - Iterates through all bottles calling `check_color()`
    - Returns True only when all tubes satisfy the goal condition

- **Level.py - Puzzle Configuration**
  - `level()`: Factory function creates initial puzzle state
  - Defines Bottle objects with starting colors and coordinates
  - Can generate multiple difficulty levels

#### View Layer (`src/View/Draw.py`)
- **Draw Module**: Rendering and visualization
  - `COLOR_MAP`: Dictionary mapping color names to RGB tuples
    - `"red": (255,0,0), "green": (0,255,0), "blue": (0,0,255)`
  - `draw_level(screen, bottles)`: Main rendering dispatcher
  - `draw_bottle(screen, bottle)`: Renders individual tube outline using `pygame.draw.lines()`
  - `draw_color(screen, cords, colors)`: Renders colored water layers
    - Calculates layer height dynamically based on tube geometry
    - Draws from bottom-up to simulate gravity
    - Renders rectangle for each color layer at correct y-coordinate


**Planned Features**:
- AI solver using A* search algorithm
- Multiple difficulty levels with procedural generation
- Move history and undo functionality
- Timer and move counter
- Hint system using heuristic-based suggestions