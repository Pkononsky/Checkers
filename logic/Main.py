from logic.Game import Game
#from logic.client_game import Client_game


def main():
    x_size = 775 # кратно 155
    y_size = 800 # кратно 40
    Game("Checkers 100", x_size, y_size, "1.png", 120).run_computer()
    #Game("Checkers 100", x_size, y_size, "1.png", 120).run_socket()
    #Client_game("Шашки 100", x_size, y_size, "1.png", 120, 5).run() скопировать проект на второй компьютер


if __name__ == '__main__':
    main()
