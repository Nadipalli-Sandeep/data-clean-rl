def get_tasks():
    return [
        {
            "id": "task1",
            "name": "Fix Missing Values",
            "description": "Reduce all missing values to zero",
            "max_steps": 10
        },
        {
            "id": "task2",
            "name": "Fix Missing + Outliers",
            "description": "Clean missing values and outliers",
            "max_steps": 15
        },
        {
            "id": "task3",
            "name": "Full Cleaning",
            "description": "Clean missing, outliers, and duplicates efficiently",
            "max_steps": 20
        }
    ]
def grade_task1(initial_missing, current_missing):
    if initial_missing == 0:
        return 1.0
    return 1 - (current_missing / initial_missing)


def grade_task2(initial_missing, current_missing, initial_outliers, current_outliers):
    missing_score = 1 - (current_missing / initial_missing) if initial_missing > 0 else 1
    outlier_score = 1 - (current_outliers / initial_outliers) if initial_outliers > 0 else 1
    return 0.5 * missing_score + 0.5 * outlier_score


def grade_task3(initial_total, current_total, steps, max_steps):
    if initial_total == 0:
        return 1.0

    quality = 1 - (current_total / initial_total)

    efficiency_bonus = (max_steps - steps) / max_steps

    return quality * (1 + efficiency_bonus)