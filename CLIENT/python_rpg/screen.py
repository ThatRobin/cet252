
class Screen:
    def __init__(self, choices, choicef):
        self.choices = choices
        self.choicef = choicef

    def display(self):
        try:
            menuChoice = int(input(str("\n".join(self.choices))))
            return self.choicef[menuChoice]
        except ValueError as e:
            self.display()
