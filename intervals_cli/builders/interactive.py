from intervals_cli.models import workout
from inquirer import List as qlist
from inquirer import prompt

questions = [
    qlist(
        "Sport",
        message="Choose Sport",
        choices=[sport.value for sport in workout.Sport],
    ),
]

answers = prompt(questions)

print(answers["Sport"] if answers else None)
