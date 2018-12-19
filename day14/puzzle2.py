import puzzle1

class RecipeSearchScoreboard(puzzle1.Scoreboard):
    def __init__(self, searchRecipe, startingScores, numElves=2):
        puzzle1.Scoreboard.__init__(self, startingScores, numElves)
        self.searchRecipe = tuple(searchRecipe)
        self.recipeFound = False
        self.foundRecipes = set()

    def tasteTest(self):
        sumOfRecipes = puzzle1.Scoreboard.tasteTest(self)
        for i in range(len(str(sumOfRecipes))):
            newRecipe = tuple(self.scores[-6-i:][:6])
            self.foundRecipes.add(newRecipe)
            if self.searchRecipe in self.foundRecipes:
                self.recipeIndex = len(self.scores) -6 -i
                self.recipeFound = True
        return sumOfRecipes