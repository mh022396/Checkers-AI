from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK, DARK_BEIGE, WHITE
from checkers.game import Game
from minimax.minimax import minimax
from minimax.alpha_beta import alpha_beta
from monte_carlo.monte_carlo_tree_search import monte_carlo_tree_search
import pygame

FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
global nodes


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():

    run = True
    pygame.font.init()

    clock = pygame.time.Clock()
    game = Game(WINDOW)
    font = pygame.font.Font('freesansbold.ttf', 20)

    neg_inf = float('-inf')
    pos_inf = float('inf')

    while run:
        clock.tick(FPS)
        depth = 6
        if game.turn == WHITE:
            #value, new_board = minimax(game.get_board(), depth, True, game, 2, WHITE, BLACK)
            #new_board = monte_carlo_tree_search(game.get_board(), True, WHITE, game, 10, 1, 6)
            value, new_board = alpha_beta(game.get_board(), depth, True, game, 2, WHITE, BLACK, neg_inf, pos_inf)
            if new_board:
                game.ai_move(new_board)
            else:
                print("WINNER: BLACK")
                game.update()
                break
            game.update()
            game.change_turn()

        # if game.turn == BLACK:
            # value, new_board = minimax(game.get_board(), depth, True, game, 2, BLACK, WHITE)
            #value, new_board = alpha_beta(game.get_board(), depth, True, game, 3, BLACK, WHITE, neg_inf, pos_inf)
            # if new_board:
            #     game.ai_move(new_board)
            # else:
            #     print("WINNER: WHITE")
            #     game.update()
            #     break
            # game.update()
            # game.change_turn()

        if game.winner():
            print("WINNER: ")
            print(("BLACK" if game.winner() == BLACK else "WHITE"))
            game.update()
            break

        text = font.render(("Black" if game.turn == BLACK else "White"), True, DARK_BEIGE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
            game.update()
        WINDOW.blit(text, (10, 10))

        game.update()
        pygame.time.delay(10)

    pygame.time.delay(10000)
    pygame.quit()


if __name__ == '__main__':
    main()
