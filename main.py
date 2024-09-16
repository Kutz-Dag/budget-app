class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        for item in self.ledger:
            amount = f"{item['amount']:.2f}"
            items += f"{item['description'][:23]:23}{amount:>7}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total

    def deposit(self, amount, description = ""):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description = ""):
        if self.check_funds(amount):
            self.ledger.append({'amount': amount * -1, 'description': description})
            return True
        return False

    def get_balance(self):
        balance = 0
        for item in self.ledger:
            balance += item["amount"]
        return balance

    def transfer(self, amount, category):
        if self.withdraw(amount, f"Transfer to {category.name}"):
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

def create_spend_chart(categories):
    
    total_spent = 0
    category_spent = []
    for category in categories:
        spent = sum(-item['amount'] for item in category.ledger if item['amount'] < 0)
        category_spent.append(spent)
        total_spent += spent

    percentages = [int((spent / total_spent) * 100) // 10 * 10 for spent in category_spent]

    bar_chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        bar_chart += f"{i:>3}|"
        for percentage in percentages:
            bar_chart += " o " if percentage >= i else "   "
        bar_chart += " \n"

    bar_chart += "    " + "-" * (3 * len(categories) + 1) + "\n"

    max_name_length = max(len(category.name) for category in categories)
    for i in range(max_name_length):
        bar_chart += "     "
        for category in categories:
            if i < len(category.name):
                bar_chart += f"{category.name[i]}  "
            else:
                bar_chart += "   "
        bar_chart += "\n"

    return bar_chart.rstrip("\n")

food = Category("Food")
clothing = Category("Clothing")
entertainment = Category("Entertainment")

food.deposit(800.70, "Cash deposit")
food.withdraw(10.15, "Groceries")
food.withdraw(15.89, "Restaurant")
food.transfer(70, clothing)

clothing.deposit(500, "Cash deposit")
clothing.withdraw(25.55, "Shoes")
clothing.withdraw(100, "Chiesa Liverpool shirt")

entertainment.deposit(90, "Cash deposit")
entertainment.withdraw(10, "Movies")

print(food)
print(clothing)
print(entertainment)

print(create_spend_chart([food, clothing, entertainment]))
