import pygame
import sys
import math
import socket
from logic.Player_checkers import Player_checkers
from logic.Computer_checkers import Computer_checkers
from collections import defaultdict
from pygame.rect import Rect


class Client_game:
    def __init__(self,
                 caption,
                 width,
                 height,
                 back_image_filename,
                 frame_rate,
                 checkers_count_line):
        self.background_image = pygame.image.load(back_image_filename)
        self.frame_rate = frame_rate
        self.game_over = False
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((width, height))
        self.bounds = Rect(0, 0, width, height)
        self.state = ""
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []
        self.mouse_handlers.append(self.handle_mouse_event)

        self.ky = int(height/20)
        self.kx = int(width/31)
        self.objects = dict()
        self.player_c = 0
        self.computer_c = 0
        if self.kx < self.ky:
            rad = self.kx
        else:
            rad = self.ky
        y = self.ky
        for i in range(0, 6):
            if i % 2 != 0:
                x = self.kx * 2
            else:
                x = self.kx * 5
            for j in range(0, 5):
                self.objects[(x, y)] = Computer_checkers(x, y, rad, (255, 0, 0))
                x += self.kx * 6
                self.computer_c += 1
            y += self.ky
        y = height - self.ky
        for i in range(0, 6):
            if i % 2 != 0:
                x = self.kx * 2
            else:
                x = self.kx * 5
            for j in range(0, 5):
                self.objects[(x, y)] = Player_checkers(x, y, rad, (0, 0, 0))
                x += self.kx * 6
                self.player_c += 1
            y -= self.ky
        self.from_c = tuple()
        self.to_c = tuple()
        self.active_checker = None
        self.enemy_dict = dict()
        self.turn = "Player"

    def draw_hexagons(self):
        y1 = self.ky
        y2 = 0
        y3 = 0
        y4 = self.ky
        y5 = self.ky * 2
        y6 = self.ky * 2
        y7 = self.ky
        for j in range(0, 19):
            if j % 2 != 0:
                x1 = 0
                x2 = self.kx
                x3 = self.kx * 3
                x4 = self.kx * 4
                x5 = self.kx * 3
                x6 = self.kx
                x7 = 0
            else:
                x1 = self.kx * 3
                x2 = self.kx * 4
                x3 = self.kx * 6
                x4 = self.kx * 7
                x5 = self.kx * 6
                x6 = self.kx * 4
                x7 = self.kx * 3
            for i in range(0, 5):
                pygame.draw.line(self.surface, (0, 0, 0), (x1, y1), (x2, y2), 5)
                pygame.draw.line(self.surface, (0, 0, 0), (x2, y2), (x3, y3), 5)
                pygame.draw.line(self.surface, (0, 0, 0), (x3, y3), (x4, y4), 5)
                pygame.draw.line(self.surface, (0, 0, 0), (x4, y4), (x5, y5), 5)
                pygame.draw.line(self.surface, (0, 0, 0), (x5, y5), (x6, y6), 5)
                pygame.draw.line(self.surface, (0, 0, 0), (x6, y6), (x7, y7), 5)
                x1 += self.kx * 6
                x2 += self.kx * 6
                x3 += self.kx * 6
                x4 += self.kx * 6
                x5 += self.kx * 6
                x6 += self.kx * 6
                x7 += self.kx * 6
            y1 += self.ky
            y2 += self.ky
            y3 += self.ky
            y4 += self.ky
            y5 += self.ky
            y6 += self.ky
            y7 += self.ky

    def draw(self):
        """
        draws all the checkers on the field
        :return:
        """
        for o in self.objects.values():
            if o is not None:
                o.draw(self.surface)

    def handle_events(self):
        """
        handles the events of closing the game and clicking the mouse
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def handle_mouse_event(self, type, pos):
        """
        selects the method of the mouse action
        :param type: - action type
        :param pos: - click position
        :return:
        """
        if type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)

    def handle_mouse_down(self, pos):
        """
        first chooses the checker then moves it to the selected position
        :param pos: - click position
        :return:
        """
        if self.bounds.collidepoint(pos):
            self.check_to_enemy("<class 'logic.Player_checkers.Player_checkers'>")
            x_pos, y_pos = self.get_true_mouthe_pos(pos)

            if str(type(self.objects.get((x_pos, y_pos)))) == "<class 'logic.Player_checkers.Player_checkers'>":
                self.active_checker = self.objects.get((x_pos, y_pos))
                return
            if self.active_checker is None:
                return
            cx_pos, cy_pos = self.active_checker.center
            if self.active_checker.checkers_type == "king" and (math.fabs(x_pos - cx_pos) >= self.kx * 3 and math.fabs(y_pos - cy_pos) >= self.ky and math.fabs(x_pos - cx_pos) // (self.kx * 3) == math.fabs(y_pos - cy_pos) // self.ky or x_pos - cx_pos == 0 and math.fabs(y_pos - cy_pos) >= self.ky * 2):
                if len(self.enemy_dict) == 0:
                    if self.objects.get((x_pos, y_pos)) is None:
                        self.move_checker((x_pos - cx_pos) // 5, (y_pos - cy_pos) // 5,  x_pos, cx_pos, y_pos, cy_pos)
                        self.turn = "Computer"
                    return
                gen_finder = self.find_enemy_for_king_on_path(x_pos, y_pos, cx_pos, cy_pos)
                if self.enemy_dict.get((x_pos, y_pos)) is None and next(gen_finder):
                    self.move_checker((x_pos - cx_pos) // 5, (y_pos - cy_pos) // 5, x_pos, cx_pos, y_pos, cy_pos)
                    self.objects[next(gen_finder)] = None
                    self.computer_c -= 1
                    self.enemy_dict.clear()
                    self.check_to_enemy("<class 'logic.Player_checkers.Player_checkers'>")
                    if len(self.enemy_dict) == 0:
                        self.active_checker = None
                        self.turn = "Computer"
                    self.enemy_dict.clear()

            if math.fabs(x_pos - cx_pos) == self.kx * 3 and math.fabs(y_pos - cy_pos) == self.ky \
                    or x_pos - cx_pos == 0 and math.fabs(y_pos - cy_pos) == self.ky * 2:
                if len(self.enemy_dict) == 0:
                    if self.objects.get((x_pos, y_pos)) is None:
                        if y_pos - cy_pos <= 0:
                            self.move_checker((x_pos - cx_pos) // 5, (y_pos - cy_pos) // 5, x_pos, cx_pos, y_pos, cy_pos)
                            if y_pos <= self.ky * 2:
                                self.active_checker.color = (40, 40, 40)
                                self.active_checker.checkers_type = "king"
                            self.active_checker = None
                            self.turn = "Computer"
                    return
                if self.enemy_dict.get((x_pos, y_pos)) is not None:
                    if x_pos - cx_pos == 0:
                        new_x_pos = x_pos
                        new_y_pos = y_pos + self.ky * 2 * int((y_pos - cy_pos) // math.fabs(y_pos - cy_pos))
                    else:
                        new_x_pos = x_pos + self.kx * 3 * int((x_pos - cx_pos) // math.fabs(x_pos - cx_pos))
                        new_y_pos = y_pos + self.ky * int((y_pos - cy_pos) // math.fabs(y_pos - cy_pos))
                    if self.objects.get((new_x_pos, new_y_pos)) is None:
                        self.move_checker(2 * (x_pos - cx_pos) // 5, 2 * (y_pos - cy_pos) // 5, new_x_pos, cx_pos, new_y_pos, cy_pos)
                        if new_y_pos <= self.ky * 2:
                            self.active_checker.color = (40, 40, 40)
                            self.active_checker.checkers_type = "king"
                        self.active_checker = None
                        self.objects[(x_pos, y_pos)] = None
                        self.computer_c -= 1
                        self.enemy_dict.clear()
                        self.check_to_enemy("<class 'logic.Player_checkers.Player_checkers'>")
                        if len(self.enemy_dict) == 0:
                            self.active_checker = None
                            self.turn = "Computer"
                        self.enemy_dict.clear()

    def get_true_mouthe_pos(self, pos):
        """
        calculates the coordinates of the checker that was clicked
        :param pos: - click position
        :return:
        """
        x_pos, y_pos = pos
        x_keys = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]
        x_left_count = 0
        x_right_count = 0
        x_left = x_pos
        x_right = x_pos
        while x_left % self.kx != 0:
            x_left -= 1
            x_left_count += 1
        while x_right % self.kx != 0:
            x_right += 1
            x_right_count += 1
        if x_left_count < x_right_count:
            x_pos = x_left
        else:
            x_pos = x_right
        if x_pos // self.kx - 1 in x_keys:
            x_pos -= self.kx
        if x_pos // self.kx + 1 in x_keys:
            x_pos += self.kx

        if x_pos // self.kx % 2 == 0:
            parity = 1
        else:
            parity = 0

        if parity != 1:
            while y_pos % self.ky != 0:
                y_pos -= 1
            if (y_pos // self.ky) % 2 == 0:
                y_pos += self.ky
        else:
            while y_pos % self.ky != 0:
                y_pos -= 1
            if (y_pos // self.ky) % 2 == 1:
                y_pos += self.ky
        return x_pos, y_pos

    def check_to_enemy(self, checker_type):
        """
        checks enemies nearby every checker of current player
        :param checker_type: - current player
        :return:
        """
        for pos, checker in self.objects.items():
            if str(type(checker)) == checker_type:
                pos_x, pos_y = pos
                if checker.checkers_type == "king":
                    self.check_enemy_for_king(pos_x, pos_y)
                else:
                    self.check_enemy_for_checker(pos_x, pos_y)

    def move_checker(self, kx, ky, x_pos, cx_pos, y_pos, cy_pos):
        """
        moves the checker to the selected position
        :param koef:
        :param x_pos: - to this position
        :param cx_pos: - from this position
        :param y_pos: - to this position
        :param cy_pos: - from this position
        :return:
        """
        self.active_checker.speed = (kx, ky)
        for i in range(0, 5):
            self.surface.blit(self.background_image, (0, 0))
            self.active_checker.update()
            self.draw_hexagons()
            self.draw()
            pygame.display.update()
        self.active_checker.speed = (0, 0)
        self.objects[(x_pos, y_pos)] = self.active_checker
        self.objects[(cx_pos, cy_pos)] = None
        self.from_c = (cx_pos, cy_pos)
        self.to_c = self.active_checker.center

    def find_enemy_for_king_on_path(self, x, y, cx, cy):
        """
        looking for enemies for checkers type king on line
        :param x: - completion point
        :param y: - completion point
        :param cx: - start point
        :param cy: - start point
        :return:
        """
        if x - cx == 0 :
            kx = 0
            ky = 2 * math.fabs(y - cy) / (y - cy)
        else:
            kx = math.fabs(x - cx) / (x - cx)
            ky = math.fabs(y - cy) / (y - cy)
        x_pos = cx
        y_pos = cy
        enemy_flag = False
        checker_flag = False
        first_friend_flag = False
        pos_x, pos_y = (0, 0)
        while self.bounds.collidepoint((x_pos, y_pos)) and y_pos != y:
            x_pos += kx * self.kx * 3
            y_pos += ky * self.ky
            if type(self.objects.get((x_pos, y_pos))) is type(self.active_checker):
                first_friend_flag = True
            if self.enemy_dict.get((x_pos, y_pos)) is not None:
                if cx < x_pos < x and cy < y_pos < y \
                        or cx > x_pos > x and cy < y_pos < y \
                        or cx < x_pos < x and cy > y_pos > y \
                        or cx > x_pos > x and cy > y_pos > y \
                        or cx == x and cy < y_pos < y \
                        or cx == x and cy > y_pos > y:
                    enemy_flag = True
                    pos_x = x_pos
                    pos_y = y_pos
                    if self.objects.get((pos_x + kx * self.kx * 3, pos_y + ky * self.ky)) is not None:
                        checker_flag = True
        if enemy_flag and not first_friend_flag and not checker_flag:
            yield True
            yield (pos_x, pos_y)
        else:
            yield False

    def check_enemy_for_checker(self, x_pos, y_pos):
        """
        looking for enemies for common type checker
        :param x_pos: - checker position
        :param y_pos: - checker position
        :return:
        """
        this_check_type = type(self.objects.get((x_pos, y_pos)))
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 or j == 0:
                    continue
                possible_enemy = self.objects.get((x_pos + i * self.kx * 3, y_pos + j * self.ky))
                if type(possible_enemy) is not this_check_type and possible_enemy is not None:
                    if self.objects.get((x_pos + i * 2 * self.kx * 3, y_pos + j * 2 * self.ky)) is None:
                        if x_pos + i * 2 * self.kx * 3 in range(1, 775) and y_pos + j * 2 * self.ky in range(1, 800):
                            self.enemy_dict[x_pos + i * self.kx * 3, y_pos + j * self.ky] = possible_enemy
        for i in range(-1, 2):
            if i == 0:
                continue
            possible_enemy = self.objects.get((x_pos, y_pos + i * self.ky * 2))
            if type(possible_enemy) is not this_check_type and possible_enemy is not None:
                if self.objects.get((x_pos, y_pos + i * 2 * self.ky * 2)) is None:
                    if y_pos + i * 2 * self.ky * 2 in range(1, 800):
                        self.enemy_dict[x_pos, y_pos + i * self.ky * 2] = possible_enemy

    def check_enemy_for_king(self, x, y):
        """
        looking for enemies for common type checker
        :param x_pos: - checker position
        :param y_pos: - checker position
        :return:
        """
        this_check_type = type(self.objects.get((x, y)))
        x_pos = x
        y_pos = y
        while self.bounds.collidepoint((x_pos, y_pos)):
            x_pos += self.kx * 3
            y_pos += self.ky
            if type(self.objects.get((x_pos, y_pos))) is this_check_type:
                break
            if type(self.objects.get((x_pos, y_pos))) is not this_check_type and self.objects.get((x_pos, y_pos)) is not None:
                if self.objects.get((x_pos + self.kx * 3, y_pos + self.ky)) is None and (self.objects.get((x_pos - self.kx * 3, y_pos - self.ky)) is None or x_pos - self.kx * 3 == x and y_pos - self.ky == y) and self.bounds.collidepoint((x_pos + self.kx * 3, y_pos + self.ky)):
                    self.enemy_dict[(x_pos, y_pos)] = self.objects.get((x_pos, y_pos))
                    break
        x_pos = x
        y_pos = y
        while self.bounds.collidepoint((x_pos, y_pos)):
            x_pos -= self.kx * 3
            y_pos += self.ky
            if type(self.objects.get((x_pos, y_pos))) is this_check_type:
                break
            if type(self.objects.get((x_pos, y_pos))) is not this_check_type and self.objects.get((x_pos, y_pos)) is not None:
                if self.objects.get((x_pos - self.kx * 3, y_pos + self.ky)) is None and (self.objects.get((x_pos + self.kx * 3, y_pos - self.ky)) is None or x_pos + self.kx * 3 == x and y_pos - self.ky == y) and self.bounds.collidepoint((x_pos - self.kx * 3, y_pos + self.ky)):
                    self.enemy_dict[(x_pos, y_pos)] = self.objects.get((x_pos, y_pos))
                    break
        x_pos = x
        y_pos = y
        while self.bounds.collidepoint((x_pos, y_pos)):
            x_pos -= self.kx * 3
            y_pos -= self.ky
            if type(self.objects.get((x_pos, y_pos))) is this_check_type:
                break
            if type(self.objects.get((x_pos, y_pos))) is not this_check_type and self.objects.get((x_pos, y_pos)) is not None:
                if self.objects.get((x_pos - self.kx * 3, y_pos - self.ky)) is None and (self.objects.get((x_pos + self.kx * 3, y_pos + self.ky)) is None or x_pos + self.kx * 3 == x and y_pos + self.ky == y) and self.bounds.collidepoint((x_pos - self.kx * 3, y_pos - self.ky)):
                    self.enemy_dict[(x_pos, y_pos)] = self.objects.get((x_pos, y_pos))
                    break
        x_pos = x
        y_pos = y
        while self.bounds.collidepoint((x_pos, y_pos)):
            x_pos += self.kx * 3
            y_pos -= self.ky
            if type(self.objects.get((x_pos, y_pos))) is this_check_type:
                break
            if type(self.objects.get((x_pos, y_pos))) is not this_check_type and self.objects.get((x_pos, y_pos)) is not None:
                if self.objects.get((x_pos + self.kx * 3, y_pos - self.ky)) is None and (self.objects.get((x_pos - self.kx * 3, y_pos + self.ky)) is None or x_pos - self.kx * 3 == x and y_pos + self.ky == y) and self.bounds.collidepoint((x_pos + self.kx * 3, y_pos - self.ky)):
                    self.enemy_dict[(x_pos, y_pos)] = self.objects.get((x_pos, y_pos))
                    break

        x_pos = x
        y_pos = y
        while self.bounds.collidepoint((x_pos, y_pos)):
            y_pos += 2 * self.ky
            if type(self.objects.get((x_pos, y_pos))) is this_check_type:
                break
            if type(self.objects.get((x_pos, y_pos))) is not this_check_type and self.objects.get((x_pos, y_pos)) is not None:
                if self.objects.get((x_pos, y_pos + 2 * self.ky)) is None and (self.objects.get((x_pos, y_pos - 2 * self.ky)) is None or y_pos - 2 * self.ky == y) and self.bounds.collidepoint((x_pos, y_pos + 2 * self.ky)):
                    self.enemy_dict[(x_pos, y_pos)] = self.objects.get((x_pos, y_pos))
                    break

        x_pos = x
        y_pos = y
        while self.bounds.collidepoint((x_pos, y_pos)):
            y_pos -= 2 * self.ky
            if type(self.objects.get((x_pos, y_pos))) is this_check_type:
                break
            if type(self.objects.get((x_pos, y_pos))) is not this_check_type and self.objects.get((x_pos, y_pos)) is not None:
                if self.objects.get((x_pos, y_pos - 2 * self.ky)) is None and (self.objects.get((x_pos, y_pos + 2 * self.ky)) is None or y_pos + 2 * self.ky == y) and self.bounds.collidepoint((x_pos, y_pos - 2 * self.ky)):
                    self.enemy_dict[(x_pos, y_pos)] = self.objects.get((x_pos, y_pos))
                    break

    def try_to_find_king(self, x, y, kx, ky):
        """
        looking for a king who can change your checker
        :return:
        """
        x_pos = x
        y_pos = y
        while self.bounds.collidepoint((x_pos, y_pos)):
            x_pos += kx * self.kx * 3
            y_pos += ky * self.ky
            if str(type(self.objects.get((x_pos, y_pos)))) == "<class 'logic.Computer_checkers.Computer_checkers'>":
                if self.objects[(x_pos, y_pos)].checkers_type == "king":
                    yield True
                    yield x_pos, y_pos
        yield False

    def another_player_move(self, pos):
        """
        makes a player move from the local network
        :param pos: - checker position that the player pushed
        :return:
        """
        to_x, to_y = pos
        from_x, from_y = self.active_checker.center
        self.move_checker((to_x - from_x) // 5, (to_y - from_y) // 5, to_x, from_x, to_y, from_y)
        if to_x - from_x == 0:
            kx = 0
        else:
            kx = math.fabs(to_x - from_x) // (to_x - from_x)
        ky = math.fabs(to_y - from_y) // (to_y - from_y)
        while from_y != to_y:
            if self.objects.get((from_x, from_y)) is not None:
                self.objects[(from_x, from_y)] = None
            from_x += kx * self.kx * 3
            from_y += ky * self.ky
        self.active_checker = None

    def run(self):
        sock = socket.socket()
        host = 'localhost'
        port = 9090
        sock.connect((host, port))
        flag = True
        while True:
            if flag:
                data = sock.recv(100000)
                data_d = data.decode().split('/')
                from_d = data_d[0].split(',')
                from_x = 775 - int(from_d[0][1:])
                from_y = 800 - int(from_d[1][:len(from_d[1]) - 1])
                to_d = data_d[1].split(',')
                to_x = 775 - int(to_d[0][1:])
                to_y = 800 - int(to_d[1][:len(to_d[1]) - 1])
                print(data)
                self.active_checker = self.objects.get((from_x, from_y))
                self.another_player_move((to_x, to_y))
                self.from_c = tuple()
                self.to_c = tuple()
                if data_d[2] == '1':
                    flag = False
                self.surface.blit(self.background_image, (0, 0))
                self.draw()
                self.draw_hexagons()
                pygame.display.update()
            if not flag:
                self.handle_events()
                self.surface.blit(self.background_image, (0, 0))
                self.draw()
                self.draw_hexagons()
                pygame.display.update()
            if self.from_c != tuple():
                if self.turn == "Player":
                    sock.send((str(self.from_c) + '/' + str(self.to_c) +
                               '/' + "0").encode())
                if self.turn == "Computer":
                    sock.send((str(self.from_c) + '/' + str(self.to_c) +
                               '/' + '1').encode())
                    flag = True
                    self.turn = "Player"
                self.from_c = tuple()
                self.to_c = tuple()
            self.clock.tick(self.frame_rate)
