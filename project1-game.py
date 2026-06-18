import random

def get_computer_choice():
    """Возвращает случайный выбор компьютера"""
    choices = ["камень", "ножницы", "бумага"]
    return random.choice(choices)

def determine_winner(player, computer):
    """Определяет победителя раунда"""
    if player == computer:
        return "ничья"
        
    winning_combinations = {
        "камень": "ножницы",
        "ножницы": "бумага",
        "бумага": "камень"
    }
    
    if winning_combinations[player] == computer:
        return "игрок"
    else:
        return "компьютер"

def main():
    """Основная логика игры"""
    # Приветствие и правила
    print("=" * 50)
    print("Добро пожаловать в игру 'Камень-Ножницы-Бумага'!")
    print("=" * 50)
    print("\nПравила игры:")
    print("• Камень бьет ножницы")
    print("• Ножницы бьют бумагу")
    print("• Бумага бьет камень")
    print("• Игра продолжается до 3 победных очков")
    print("\n" + "=" * 50)
    
    # Инициализация счета
    player_score = 0
    computer_score = 0
    round_number = 1
    
    # Основной игровой цикл
    while player_score < 3 and computer_score < 3:
        print(f"\nРаунд {round_number}")
        print("-" * 30)
        
        # Запрос выбора игрока
        while True:
            player_choice = input("Ваш выбор (камень/ножницы/бумага): ").lower().strip()
            if player_choice in ["камень", "ножницы", "бумага"]:
                break
            else:
                print("Ошибка! Введите 'камень', 'ножницы' или 'бумага'.")
                
        # Выбор компьютера
        computer_choice = get_computer_choice()
        print(f"Компьютер выбрал: {computer_choice}")
        
        # Определение победителя раунда
        winner = determine_winner(player_choice, computer_choice)
        
        # Обновление счета
        if winner == "игрок":
            player_score += 1
            print("Вы выиграли этот раунд!")
        elif winner == "компьютер":
            computer_score += 1
            print("Компьютер выиграл этот раунд!")
        else:
            print("Ничья!")
            
        # Показать текущий счет
        print("\nТекущий счет:")
        print(f"Игрок: {player_score} | Компьютер: {computer_score}")
        print("-" * 30)
        
        round_number += 1
        
    # Определение и вывод итогового результата
    print("\n" + "=" * 50)
    print("ИГРА ОКОНЧЕНА!")
    print("=" * 50)
    
    if player_score > computer_score:
        print(f"\n🎉 ПОБЕДА! Вы выиграли со счетом {player_score}:{computer_score}")
    else:
        print(f"\n💻 ПОБЕДА КОМПЬЮТЕРА! Счет {computer_score}:{player_score}")
        
    # Прощальное сообщение
    print("\nСпасибо за игру!")

# Запуск игры
if name == "main":
    main()
