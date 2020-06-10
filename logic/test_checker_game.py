import unittest
from unittest import TestCase
from unittest.mock import MagicMock

import logic
import pygame
from coverage import coverage
from logic.Computer_checkers import Computer_checkers
from logic.Game import Game
from logic.Main import main
from logic.Player_checkers import Player_checkers
from logic.client_game import Client_game
from logic.game_object import GameObject


class Tests(TestCase):

    def test_game_object_init(self):
        game_obj = GameObject(5, 5, 10, 10)
        self.assertTrue(True)

    def test_game_object_center(self):
        game_obj = GameObject(5, 5, 10, 10)
        self.assertEqual((10, 10), game_obj.center)

    def test_game_object_move(self):
        game_obj = GameObject(5, 5, 10, 10)
        game_obj.move(1, 1)
        self.assertEqual((11, 11), game_obj.center)

    def test_game_object_update(self):
        game_obj = GameObject(5, 5, 10, 10)
        game_obj.update()
        game_obj.speed = (1, 1)
        game_obj.update()
        self.assertEqual((11, 11), game_obj.center)

    def test_Player_checkers_init(self):
        checker = Player_checkers(0, 0, 10, (0, 0, 0))
        self.assertTrue(True)

    def test_Player_checkers_draw(self):
        checker = Player_checkers(0, 0, 10, (0, 0, 0))
        checker.draw(pygame.display.set_mode((775, 800)))
        self.assertTrue(True)

    def test_Computer_checkers_init(self):
        checker = Computer_checkers(0, 0, 10, (0, 0, 0))
        self.assertTrue(True)

    def test_Computer_checkers_draw(self):
        checker = Computer_checkers(0, 0, 10, (0, 0, 0))
        checker.draw(pygame.display.set_mode((775, 800)))
        self.assertTrue(True)

    def test_game_init(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        self.assertTrue(True)

    def test_game_draw_hexagons(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.draw_hexagons()
        self.assertTrue(True)

    def test_game_draw(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.draw()
        self.assertTrue(True)

    def test_game_handle_events(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.handle_events()
        self.assertTrue(True)

    def test_game_handle_mouse_event(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.handle_mouse_event(pygame.MOUSEBUTTONDOWN, (0, 0))
        self.assertTrue(True)

    def test_game_handle_mouse_down_get_active_checker(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 2, game.ky)] = Player_checkers(game.kx * 2,
                                                               game.ky,
                                                               game.kx,
                                                               (0, 0, 0))
        game.handle_mouse_down((game.kx * 2, game.ky))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 2, game.ky)))

    def test_game_handle_mouse_down_move_checker_up(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        game.handle_mouse_down((game.kx * 5, game.ky * 2))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 5, game.ky * 2))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 5, game.ky * 2)))

    def test_game_handle_mouse_down_move_checker_up_right(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        game.handle_mouse_down((game.kx * 8, game.ky * 3))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 8, game.ky * 3))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 8, game.ky * 3)))

    def test_game_handle_mouse_down_move_checker_up_left(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        game.handle_mouse_down((game.kx * 2, game.ky * 3))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 2, game.ky * 3))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 2, game.ky * 3)))

    def test_game_handle_mouse_down_move_and_eat_checker_up(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 6)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 6,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)] = Computer_checkers(
            game.kx * 5, game.ky * 4, game.kx, (255, 0, 0))
        game.handle_mouse_down((game.kx * 5, game.ky * 6))
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 5, game.ky * 2))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 5, game.ky * 2)))

    def test_game_handle_mouse_down_move_and_eat_checker_up_left(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 8, game.ky * 5)] = Player_checkers(game.kx * 8,
                                                                   game.ky * 5,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)] = Computer_checkers(
            game.kx * 5, game.ky * 4, game.kx, (255, 0, 0))
        game.handle_mouse_down((game.kx * 8, game.ky * 5))
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 2, game.ky * 3))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 2, game.ky * 3)))

    def test_game_handle_mouse_down_move_and_eat_checker_down_left(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 8, game.ky * 3)] = Player_checkers(game.kx * 8,
                                                                   game.ky * 3,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)] = Computer_checkers(
            game.kx * 5, game.ky * 4, game.kx, (255, 0, 0))
        game.handle_mouse_down((game.kx * 8, game.ky * 3))
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 2, game.ky * 5))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 2, game.ky * 5)))

    def test_game_handle_mouse_down_move_and_eat_checker_down(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 2)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 2,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)] = Computer_checkers(
            game.kx * 5, game.ky * 4, game.kx, (255, 0, 0))
        game.handle_mouse_down((game.kx * 5, game.ky * 2))
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 5, game.ky * 6))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 5, game.ky * 6)))

    def test_game_handle_mouse_down_move_and_eat_checker_down_right(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 2, game.ky * 3)] = Player_checkers(game.kx * 2,
                                                                   game.ky * 3,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)] = Computer_checkers(
            game.kx * 5, game.ky * 4, game.kx, (255, 0, 0))
        game.handle_mouse_down((game.kx * 2, game.ky * 3))
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 8, game.ky * 5))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 8, game.ky * 5)))

    def test_game_handle_mouse_down_move_and_eat_checker_up_right(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 2, game.ky * 5)] = Player_checkers(game.kx * 2,
                                                                   game.ky * 5,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)] = Computer_checkers(
            game.kx * 5, game.ky * 4, game.kx, (255, 0, 0))
        game.handle_mouse_down((game.kx * 2, game.ky * 5))
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 8, game.ky * 3))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 8, game.ky * 3)))

    def test_game_handle_mouse_down_move_checker_up_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)].checkers_type = "king"
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        game.handle_mouse_down((game.kx * 5, game.ky * 2))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 5, game.ky * 2))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 5, game.ky * 2)))

    def test_game_handle_mouse_down_move_checker_up_right_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)].checkers_type = "king"
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        game.handle_mouse_down((game.kx * 8, game.ky * 3))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 8, game.ky * 3))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 8, game.ky * 3)))

    def test_game_handle_mouse_down_move_checker_up_left_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)].checkers_type = "king"
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        game.handle_mouse_down((game.kx * 2, game.ky * 3))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 2, game.ky * 3))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 2, game.ky * 3)))

    def test_game_handle_mouse_down_move_checker_down_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)].checkers_type = "king"
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        game.handle_mouse_down((game.kx * 5, game.ky * 6))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 5, game.ky * 6))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 5, game.ky * 6)))

    def test_game_handle_mouse_down_move_checker_down_right_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)].checkers_type = "king"
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        game.handle_mouse_down((game.kx * 8, game.ky * 5))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 8, game.ky * 5))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 8, game.ky * 5)))

    def test_game_handle_mouse_down_move_checker_down_left_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)].checkers_type = "king"
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        game.handle_mouse_down((game.kx * 2, game.ky * 5))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 2, game.ky * 5))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 2, game.ky * 5)))

    def test_game_handle_mouse_down_move_and_eat_checker_up_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 6)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 6,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 6)].checkers_type = "king"
        game.objects[(game.kx * 5, game.ky * 4)] = Computer_checkers(
            game.kx * 5, game.ky * 4, game.kx, (255, 0, 0))
        game.handle_mouse_down((game.kx * 5, game.ky * 6))
        game.handle_mouse_down((game.kx * 5, game.ky * 2))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 5, game.ky * 2))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 5, game.ky * 2)))

    def test_game_handle_mouse_down_move_and_eat_checker_up_left_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 8, game.ky * 5)] = Player_checkers(game.kx * 8,
                                                                   game.ky * 5,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 8, game.ky * 5)].checkers_type = "king"
        game.objects[(game.kx * 5, game.ky * 4)] = Computer_checkers(
            game.kx * 5, game.ky * 4, game.kx, (255, 0, 0))
        game.handle_mouse_down((game.kx * 8, game.ky * 5))
        game.handle_mouse_down((game.kx * 2, game.ky * 3))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 2, game.ky * 3))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 2, game.ky * 3)))

    def test_game_handle_mouse_down_move_and_eat_checker_down_left_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 8, game.ky * 3)] = Player_checkers(game.kx * 8,
                                                                   game.ky * 3,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 8, game.ky * 3)].checkers_type = "king"
        game.objects[(game.kx * 5, game.ky * 4)] = Computer_checkers(
            game.kx * 5, game.ky * 4, game.kx, (255, 0, 0))
        game.handle_mouse_down((game.kx * 8, game.ky * 3))
        game.handle_mouse_down((game.kx * 2, game.ky * 5))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 2, game.ky * 5))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 2, game.ky * 5)))

    def test_game_handle_mouse_down_move_and_eat_checker_down_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 2)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 2,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 2)].checkers_type = "king"
        game.objects[(game.kx * 5, game.ky * 4)] = Computer_checkers(
            game.kx * 5, game.ky * 4, game.kx, (255, 0, 0))
        game.handle_mouse_down((game.kx * 5, game.ky * 2))
        game.handle_mouse_down((game.kx * 5, game.ky * 6))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 5, game.ky * 6))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 5, game.ky * 6)))

    def test_game_handle_mouse_down_move_and_eat_checker_down_right_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 2, game.ky * 3)] = Player_checkers(game.kx * 2,
                                                                   game.ky * 3,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 2, game.ky * 3)].checkers_type = "king"
        game.objects[(game.kx * 5, game.ky * 4)] = Computer_checkers(
            game.kx * 5, game.ky * 4, game.kx, (255, 0, 0))
        game.handle_mouse_down((game.kx * 2, game.ky * 3))
        game.handle_mouse_down((game.kx * 8, game.ky * 5))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 8, game.ky * 5))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 8, game.ky * 5)))

    def test_game_handle_mouse_down_move_and_eat_checker_up_right_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 2, game.ky * 5)] = Player_checkers(game.kx * 2,
                                                                   game.ky * 5,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 2, game.ky * 5)].checkers_type = "king"
        game.objects[(game.kx * 5, game.ky * 4)] = Computer_checkers(
            game.kx * 5, game.ky * 4, game.kx, (255, 0, 0))
        game.handle_mouse_down((game.kx * 2, game.ky * 5))
        game.handle_mouse_down((game.kx * 8, game.ky * 3))
        self.assertEqual(game.active_checker, None)
        game.handle_mouse_down((game.kx * 8, game.ky * 3))
        self.assertEqual(game.active_checker,
                         game.objects.get((game.kx * 8, game.ky * 3)))

    def test_game_get_true_mouthe_pos(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        self.assertEqual(
            game.get_true_mouthe_pos((game.kx * 2 - 1, game.ky - 1)),
            (game.kx * 2, game.ky))
        self.assertEqual(
            game.get_true_mouthe_pos((game.kx * 2 + 1, game.ky - 1)),
            (game.kx * 2, game.ky))
        self.assertEqual(
            game.get_true_mouthe_pos((game.kx * 2 - 1, game.ky + 1)),
            (game.kx * 2, game.ky))
        self.assertEqual(
            game.get_true_mouthe_pos((game.kx * 2 + 1, game.ky + 1)),
            (game.kx * 2, game.ky))
        self.assertEqual(
            game.get_true_mouthe_pos((game.kx * 5 - 1, game.ky * 2 - 1)),
            (game.kx * 5, game.ky * 2))
        self.assertEqual(
            game.get_true_mouthe_pos((game.kx * 5 + 1, game.ky * 2 - 1)),
            (game.kx * 5, game.ky * 2))
        self.assertEqual(
            game.get_true_mouthe_pos((game.kx * 5 - 1, game.ky * 2 + 1)),
            (game.kx * 5, game.ky * 2))
        self.assertEqual(
            game.get_true_mouthe_pos((game.kx * 5 + 1, game.ky * 2 + 1)),
            (game.kx * 5, game.ky * 2))

    def test_game_computer_turn_move_checker(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 2)] = Computer_checkers(
            game.kx * 5, game.ky * 2, game.kx, (255, 0, 0))
        game.objects[(game.kx * 5, game.ky * 6)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 6,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 8)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 8,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.computer_turn()
        game.computer_turn()
        self.assertEqual(None, game.objects.get((game.kx * 5, game.ky * 4)))

    def test_game_computer_turn_move_checker_become_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 18)] = Computer_checkers(
            game.kx * 5, game.ky * 18, game.kx, (255, 0, 0))
        game.computer_turn()
        game.computer_turn()
        game.computer_turn()
        self.assertTrue(True)

    def test_game_computer_turn_cant_move(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 2, game.ky)] = Computer_checkers(game.kx * 2,
                                                                 game.ky,
                                                                 game.kx,
                                                                 (255, 0, 0))
        game.objects[(game.kx * 2, game.ky * 3)] = Player_checkers(game.kx * 2,
                                                                   game.ky * 3,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 2, game.ky * 5)] = Player_checkers(game.kx * 2,
                                                                   game.ky * 5,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 5, game.ky * 2)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 2,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 8, game.ky * 3)] = Player_checkers(game.kx * 8,
                                                                   game.ky * 3,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.computer_turn()
        self.assertTrue(game.objects[(game.kx * 2, game.ky)] is not None)

    def test_game_computer_turn_move_and_eat_checker_up(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 6)] = Computer_checkers(
            game.kx * 5, game.ky * 6, game.kx, (255, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.computer_turn()
        self.assertTrue(game.objects[(game.kx * 5, game.ky * 4)] is None)

    def test_game_computer_turn_down_move_and_eat_checker_up_left(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 8, game.ky * 5)] = Computer_checkers(
            game.kx * 8, game.ky * 5, game.kx, (255, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.computer_turn()
        self.assertTrue(game.objects[(game.kx * 5, game.ky * 4)] is None)

    def test_game_computer_turn_move_and_eat_checker_down_left(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 8, game.ky * 3)] = Computer_checkers(
            game.kx * 8, game.ky * 3, game.kx, (255, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.computer_turn()
        self.assertTrue(game.objects[(game.kx * 5, game.ky * 4)] is None)

    def test_game_computer_turn_move_and_eat_checker_down(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 2)] = Computer_checkers(
            game.kx * 5, game.ky * 2, game.kx, (255, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.computer_turn()
        self.assertTrue(game.objects[(game.kx * 5, game.ky * 4)] is None)

    def test_game_computer_turn_move_and_eat_checker_down_right(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 2, game.ky * 3)] = Computer_checkers(
            game.kx * 2, game.ky * 3, game.kx, (255, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.computer_turn()
        self.assertTrue(game.objects[(game.kx * 5, game.ky * 4)] is None)

    def test_game_computer_turn_move_and_eat_checker_up_right(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 2, game.ky * 5)] = Computer_checkers(
            game.kx * 2, game.ky * 5, game.kx, (255, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.computer_turn()
        self.assertTrue(game.objects[(game.kx * 5, game.ky * 4)] is None)

    def test_game_computer_turn_move_and_eat_checker_up_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 6)] = Computer_checkers(
            game.kx * 5, game.ky * 6, game.kx, (255, 0, 0))
        game.objects[(game.kx * 5, game.ky * 6)].checkers_type = "king"
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.computer_turn()
        self.assertTrue(game.objects[(game.kx * 5, game.ky * 4)] is None)

    def test_game_computer_turn_move_and_eat_checker_up_left_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 8, game.ky * 5)] = Computer_checkers(
            game.kx * 8, game.ky * 5, game.kx, (255, 0, 0))
        game.objects[(game.kx * 8, game.ky * 5)].checkers_type = "king"
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.computer_turn()
        self.assertTrue(game.objects[(game.kx * 5, game.ky * 4)] is None)

    def test_game_computer_turn_move_and_eat_checker_down_left_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 8, game.ky * 3)] = Computer_checkers(
            game.kx * 8, game.ky * 3, game.kx, (255, 0, 0))
        game.objects[(game.kx * 8, game.ky * 3)].checkers_type = "king"
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.computer_turn()
        self.assertTrue(game.objects[(game.kx * 5, game.ky * 4)] is None)

    def test_game_computer_turn_move_and_eat_checker_down_king(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.objects[(game.kx * 5, game.ky * 2)] = Computer_checkers(
            game.kx * 5, game.ky * 2, game.kx, (255, 0, 0))
        game.objects[(game.kx * 5, game.ky * 2)].checkers_type = "king"
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.computer_turn()
        self.assertTrue(game.objects[(game.kx * 5, game.ky * 4)] is None)

    def test_game_run_computer(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.player_c = 1
        game.computer_c = 1
        game.objects[(game.kx * 5, game.ky * 2)] = Computer_checkers(
            game.kx * 5, game.ky * 2, game.kx, (255, 0, 0))
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.turn = "Computer"
        game.run_computer()
        self.assertTrue(True)

    def test_game_run_heroku(self):
        x_size = 775
        y_size = 800
        game = Game("Checkers 100", x_size, y_size, "1.png", 120)
        game.objects = dict()
        game.player_c = 1
        game.computer_c = 1
        game.objects[(game.kx * 5, game.ky * 4)] = Player_checkers(game.kx * 5,
                                                                   game.ky * 4,
                                                                   game.kx,
                                                                   (0, 0, 0))
        game.objects[(game.kx * 8, game.ky)] = Computer_checkers(game.kx * 8,
                                                                 game.ky,
                                                                 game.kx,
                                                                 (255, 0, 0))
        game.handle_mouse_down((game.kx * 5, game.ky * 4))
        game.handle_events = MagicMock(
            return_value=game.handle_mouse_down((game.kx * 5, game.ky * 2)))
        conf = dict()
        conf['0'] = str(775 - game.kx * 8) + '-' + str(
            800 - game.ky) + '-' + str(
            775 - game.kx * 2) + '-' + str(800 - game.ky * 3) + '-0'
        game.get_config = MagicMock(return_value=conf)
        game.run_heroku()
        self.assertTrue(True)


if __name__ == '__main__':
    cover = coverage()
    cover.erase()
    try:
        cover.start()
        unittest.main()
    finally:
        cover.stop()
        cover.report([logic.Game, logic.game_object, logic.Player_checkers,
                      logic.Computer_checkers])
