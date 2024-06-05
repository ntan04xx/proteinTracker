class UserProfile:
    def __init__(self, age, weight, height, gender, activity, goal):
        self.age = age
        self.weight = weight
        self.height = height
        self.gender = gender
        self.activity = activity
        self.goal = goal

    def find_targets(self):
        if self.gender == 'M':
            bmr = 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)
        else:
            bmr = 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.33 * self.age)
        
        if self.activity == 'None':
            bmr *= 1.2
        elif self.activity == 'Low':
            bmr *= 1.375
        elif self.activity == 'Medium':
            bmr *= 1.55
        elif self.activity == 'High':
            bmr *= 1.725

        goal = self.goal.split(" ")
        style = goal[0]
        percent = float(goal[1])

        if style == 'Cut':
            calorie_target = bmr * (1 - percent)
            protein_target = calorie_target * 0.3 # based on https://www.bulk.com/uk/the-core/how-to-decide-your-own-macro-split/
            fat_target = calorie_target * 0.3
        elif style == 'Bulk':
            calorie_target = bmr * (1 + percent)
            protein_target = calorie_target * 0.25
            fat_target= calorie_target * 0.25
        
        return (calorie_target, protein_target, fat_target)