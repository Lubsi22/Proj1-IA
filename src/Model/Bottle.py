## @file Bottle.py
#  @brief Model class representing a single bottle in the Water Sort puzzle.
#
#  A bottle holds an ordered stack of colors and exposes the geometry
#  needed for rendering and click detection.  The bottom of the stack
#  is index 0; the top (most recently added) color is the last element.
class Bottle:

    ## @brief Constructs a Bottle with its color contents and screen geometry.
    #
    #  The screen coordinates are derived from the four corner points supplied
    #  in @p cords, which must be ordered as: top-left, bottom-left,
    #  bottom-right, top-right.
    #
    #  @param colors          List of color name strings stacked bottom-to-top
    #                         (e.g. ["red", "blue", "blue"]).
    #  @param cords           List of four (x, y) tuples defining the bottle's
    #                         bounding rectangle corners in screen space.
    #  @param capacity        Maximum number of color units the bottle can hold.
    #  @param visual_capacity Number of slots used for rendering layer heights.
    #                         Defaults to @p capacity when not provided, but may
    #                         be set to the level's global maximum so all bottles
    #                         share a uniform visual height.
    def __init__(self, colors, cords, capacity, visual_capacity=None):
        self.colors = colors
        self.cords = cords
        self.capacity = capacity
        self.visual_capacity = visual_capacity if visual_capacity is not None else capacity

        self.x = cords[0][0]
        self.y = cords[0][1]
        self.width = cords[3][0] - cords[0][0]
        self.height = cords[1][1] - cords[0][1]

    ## @brief Compares two bottles for equality by their full attribute dictionaries.
    #
    #  Used by the search algorithms when checking visited states and by
    #  select_bottle to identify whether the clicked bottle is already selected.
    #
    #  @param other The object to compare against.
    #  @return True if @p other is a Bottle with identical attributes, False otherwise.
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    
    ## @brief Returns a human-readable string showing the bottle's color stack.
    #
    #  Used when printing solution paths to the console or output files.
    #
    #  @return A string representation of the colors list (e.g. "['red', 'blue']").
        return str(self.colors)   
    def __str__(self):
        return str(self.colors) #+ ", " + str(self.cords)

    ## @brief Checks whether this bottle satisfies the win condition.
    #
    #  A bottle is considered solved if it is either:
    #  - completely empty, or
    #  - filled to capacity with a single uniform color.
    #
    #  A partially filled bottle, even with uniform color, is not solved
    #  because colors from other bottles may still need to be moved into it.
    #
    #  @return True if the bottle is empty or uniformly full, False otherwise.
    def check_color(self):
        if len(self.colors) == 0:
            return True
        if len(self.colors) != self.capacity:
            return False
        color_bottle = self.colors[0]
        for color in self.colors[1:]:
            if color != color_bottle:
                return False

        return True