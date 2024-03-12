from collections import deque
import time
import pygame
import sys
from pygame.locals import *
import easygui

# Zbog velicine zipovanog fajla koji se predaje,nedostaje fajl lib koji je sadrzao pakete

def initialize():
    pygame.init()
class CustomImage:
    def __init__(self, path, color, size):
        self.original_image = pygame.image.load(path)
        self.original_image = pygame.transform.scale(self.original_image, (size - 10, size - 10))
        self.color = color
def setup_window():
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("BYTE BOARD")
    return screen

def choose_board_size_dialog():
    pygame.font.init()
    font = pygame.font.SysFont(None, 30)

    dialog_width, dialog_height = 300, 250
    dialog_screen = pygame.display.set_mode((dialog_width, dialog_height))
    pygame.display.set_caption("Choose board size")

    button_rect1 = pygame.Rect(50, 20, 200, 50)
    button_rect2 = pygame.Rect(50, 80, 200, 50)
    button_rect5 = pygame.Rect(50, 140, 200, 50)


    running = True
    selected_size = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_rect1.collidepoint(x, y):
                    selected_size = 8
                    running = False
                elif button_rect2.collidepoint(x, y):
                    selected_size = 10
                    running = False

                elif button_rect5.collidepoint(x, y):
                    selected_size = 16
                    running = False

        dialog_screen.fill((255, 255, 255))

        pygame.draw.rect(dialog_screen, (200, 200, 200), button_rect1)
        pygame.draw.rect(dialog_screen, (200, 200, 200), button_rect2)

        pygame.draw.rect(dialog_screen, (200, 200, 200), button_rect5)

        text_8x8 = font.render('8x8', True, (0, 0, 0))
        text_10x10 = font.render('10x10', True, (0, 0, 0))

        text_16x16 = font.render('16x16', True, (0, 0, 0))

        dialog_screen.blit(text_8x8, (120, 35))
        dialog_screen.blit(text_10x10, (110, 95))

        dialog_screen.blit(text_16x16, (110, 155))

        pygame.display.flip()

    return selected_size


def GoodMoves(board, color):
    good = {}

    pozicija=[]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if len(board[i][j]) != 0:
                for index in range(len(board[i][j])):
                    if board[i][j][index].color == color:
                        figure_index = (i, j, index)
                        pozicija.append(figure_index)
                        prazna, puna = get_diagonal_neighbors(board, i, j)
                        good[figure_index] = {'puna': [], 'prazna': []}
                        if puna != []:
                            for p in puna:
                                row=p[0]
                                col=p[1]

                                if index <= len(board[row][col]):
                                    good[figure_index]['puna'].append(p)
                        elif prazna != []:
                            for pr in prazna:
                                row=pr[0]
                                col=pr[1]
                                provera = contains_path_to_nearest_stacks(board, i, j, row, col)
                                print(provera)
                                if provera:
                                    good[figure_index]['prazna'].append(pr)

    print('Dobar potez boja ' + str(color) + str(good))
    # print(pozicija)
    return good

def new_states(good_moves, startRow, startCol, index):
    key = (startRow, startCol, index)

    if key in good_moves:
        print('Dobar potez '+str(good_moves[key]))
        return good_moves[key]

    else:
        return {'puna': [], 'prazna': []}


def evaluate_state(board, color):
    result = GoodMoves(board, color)
    new_dict = {}

    for key in result:


        print("Key:", key)
        i, j, index = key
        duzina = len(board[i][j]) - 1
        if (board[i][j][duzina].color == color):
            print(str(i) + str(j) + str(index))

            # Accessing values for the current key
            values_for_key = result[key]


            if all(len(subvalue) == 0 for subkey, subvalue in values_for_key.items()):
                print("All subkeys are empty. Skipping...")
                continue

            new_dict[key] = {}

            for subkey, subvalue in values_for_key.items():


                # Check if subvalue is a list before attempting unpacking
                if isinstance(subvalue, list):
                    new_values = []
                    for tuple_value in subvalue:
                        row, col = tuple_value

                        # Calculate the new value based on lengths
                        new_value = len(board[i][j]) - index + len(board[row][col])
                        new_values.append(new_value)

                    # Assign the new values to the new dictionary
                        new_dict[key][tuple_value] = new_value

                else:
                    print("Invalid subvalue:", subvalue)
        elif(not new_dict):
                print(str(i) + str(j) + str(index))

                # Accessing values for the current key
                values_for_key = result[key]

                if all(len(subvalue) == 0 for subkey, subvalue in values_for_key.items()):
                    print("All subkeys are empty. Skipping...")
                    continue

                new_dict[key] = {}

                for subkey, subvalue in values_for_key.items():

                    # Check if subvalue is a list before attempting unpacking
                    if isinstance(subvalue, list):
                        new_values = []
                        for tuple_value in subvalue:
                            row, col = tuple_value

                            # Calculate the new value based on lengths
                            new_value = len(board[i][j]) - index + len(board[row][col])
                            new_values.append(new_value)


                            new_dict[key][tuple_value] = new_value

                    else:
                        print("Invalid subvalue:", subvalue)

    print("New Dictionary:", new_dict)
    return new_dict

def find_max_entries(evaluated_dict):
    max_entries = []
    max_value = float('-inf')


    for key, sub_dict in evaluated_dict.items():
        if sub_dict:
            current_max_value = max(sub_dict.values())
            max_value = max(max_value, current_max_value)


    for key, sub_dict in evaluated_dict.items():
        if sub_dict and max_value in sub_dict.values():
            max_entries.append((key, sub_dict))
    print('Max je:',max_entries)
    return max_entries

def find_min_entries(evaluated_dict):
    min_entries = []
    min_value = float('+inf')  # Initialize to negative infinity to ensure any value is greater

    # Find the maximum new value
    for key, sub_dict in evaluated_dict.items():
        if sub_dict:
            current_min_value = min(sub_dict.values())
            min_value = min(min_value, current_min_value)

    # Collect all entries with the maximum new value
    for key, sub_dict in evaluated_dict.items():
        if sub_dict and min_value in sub_dict.values():
            min_entries.append((key, sub_dict))
    print('Min je:',min_entries)
    return min_entries




def choose_color_dialog():
    pygame.font.init()
    font = pygame.font.SysFont(None, 30)

    dialog_width, dialog_height = 300, 150
    dialog_screen = pygame.display.set_mode((dialog_width, dialog_height))
    pygame.display.set_caption("Choose color")

    button_rect1 = pygame.Rect(50, 20, 200, 50)
    button_rect2 = pygame.Rect(50, 80, 200, 50)

    running = True
    selected_color = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_rect1.collidepoint(x, y):
                    selected_color = 'BLACK'
                    running = False
                elif button_rect2.collidepoint(x, y):
                    selected_color = 'WHITE'
                    running = False

        dialog_screen.fill((255, 255, 255))

        pygame.draw.rect(dialog_screen, (200, 200, 200), button_rect1)
        pygame.draw.rect(dialog_screen, (200, 200, 200), button_rect2)

        text_8x8 = font.render('BLACK', True, (0, 0, 0))
        text_16x16 = font.render('WHITE', True, (0, 0, 0))

        dialog_screen.blit(text_8x8, (120, 35))
        dialog_screen.blit(text_16x16, (110, 95))

        pygame.display.flip()
    print(selected_color)
    return selected_color

def draw_board(screen, cell_size, n):
    white = (240, 229, 170)
    gray = (128, 128, 128)

    for row in range(n):
        for col in range(n):
            color = white if (row + col) % 2 == 1 else gray
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
import pygame
import sys

def show_selected_piece_window(selected_piece, board, screen, cell_size):
    row, col = selected_piece
    pieces = board[row][col]

    dialog_width, dialog_height = 200, 200
    row_height = dialog_height // 8  # Visina svakog reda

    main_dialog_x = col * cell_size
    main_dialog_y = row * cell_size

    dialog_x_main = main_dialog_x
    dialog_y_main = main_dialog_y

    if col < len(board[0]) // 2:
        dialog_x_side = dialog_x_main + 2 * cell_size
    else:
        dialog_x_side = dialog_x_main - dialog_width - cell_size

    dialog_y_side = dialog_y_main

    dialog_rect = pygame.Rect(dialog_x_side, dialog_y_side, dialog_width, dialog_height)
    pygame.draw.rect(screen, (255, 255, 255), dialog_rect)

    font = pygame.font.SysFont(None, 20)

    selected_row = None

    while True:
        for i, piece in enumerate(reversed(pieces)):
            offset = i * 13.5214
            text = font.render(f"{len(pieces) - i}. {piece.color} figura", True, (0, 0, 0))

            if len(pieces) > i:
                pygame.draw.rect(screen, (211, 211, 211), (dialog_x_side, dialog_y_side + 10 + i * 20, dialog_width, 20))

                if i == selected_row:
                    pygame.draw.rect(screen, (0, 0, 255), (dialog_x_side, dialog_y_side + 10 + i * 20, dialog_width, 20))
                    for s in range(0, i):

                        pygame.draw.rect(screen, (0, 0, 255),
                                         (dialog_x_side, dialog_y_side + 10 + s * 20, dialog_width, 20))
                        text = font.render(f"{len(pieces)-s}. {piece.color} figura", True, (255, 0, 0))

                        screen.blit(text, (dialog_x_side + 10, dialog_y_side + 10 + s * 20))
                if pygame.Rect(dialog_x_side + 10, dialog_y_side + 10 + i * 20, dialog_width, 20).collidepoint(
                        pygame.mouse.get_pos()):
                    text = font.render(f"{len(pieces) - i}. {piece.color} figura", True, (255, 0, 0))

                screen.blit(text, (dialog_x_side + 10, dialog_y_side + 10 + i * 20))


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if dialog_rect.collidepoint(x, y):
                    clicked_row = (y - dialog_y_side - 10) // 20

                    if 0 <= clicked_row < len(pieces):
                        if clicked_row == selected_row:
                            # Ako je ponovljeno kliknuto na isti red, deselektuj ga
                            selected_row = None
                        else:
                            selected_row = clicked_row


                else:

                    return 0 if selected_row is None else len(pieces)-1-selected_row   # Ako korisnik klikne van dijaloga, zatvori dijalog

        pygame.display.flip()







def draw_labels(screen, cell_size, n):
    font = pygame.font.SysFont(None, 20)

    # Ispisi slova
    for i in range(n):
        letter = chr(ord('A') + i)
        text = font.render(letter, True, (0, 0, 0))
        screen.blit(text, (0, i * cell_size + cell_size // 2 ))

    # Ispisi brojeve
    for i in range(0, n):
        number = str(i+1)
        text = font.render(number, True, (0, 0, 0))
        screen.blit(text, (i * cell_size + cell_size // 2 - cell_size//5, 0))


def load_and_resize_images(cell_size):
    image1 = CustomImage("bela_figura.png", "white", cell_size)
    image2 = CustomImage("crna_figura.png", "black", cell_size)

    return image1, image2

# U funkciji create_board:
def create_board(cell_size, n):
    image1, image2 = load_and_resize_images(cell_size)

    # Inicijalizacija prazne table
    board = [[[] for _ in range(n)] for _ in range(n)]

    # Postavljanje slika na početne pozicije
    for row in range(n):
        for col in range(n):
            if row % 2 == 0 and row != 0 and row != n - 1 and col % 2 == 0:
                board[row][col].append(CustomImage("bela_figura.png", "white", cell_size))
            elif row % 2 == 1 and col % 2 == 1 and row != 0 and row != n - 1:
                board[row][col].append(CustomImage("crna_figura.png", "black", cell_size))

    return board
# def IsEmpty(board, startRow, startCol):
#
#     susedi = get_diagonal_neighbors(board, startRow, startCol)
#
#
#     return prazna_susedna_polja



def get_diagonal_neighbors(board, row, col):
    if board[row][col]:
        neighbors = []

        # Gornji levi sused
        if row > 0 and col > 0:
            neighbors.append((row - 1, col - 1))

        # Gornji desni sused
        if row > 0 and col < len(board[0]) - 1:
            neighbors.append((row - 1, col + 1))

        # Donji levi sused
        if row < len(board) - 1 and col > 0:
            neighbors.append((row + 1, col - 1))

        # Donji desni sused
        if row < len(board) - 1 and col < len(board[0]) - 1:
            neighbors.append((row + 1, col + 1))
        prazna_susedna_polja = []
        puna_susedna_polja = []
        for sused in neighbors:
            row, col = sused
            if len(board[row][col]) == 0:
                prazna_susedna_polja.append(sused)
            else:
                puna_susedna_polja.append(sused)

        # print('Prazna polja: ' + str(prazna_susedna_polja))
        # print('Puna polja: ' + str(puna_susedna_polja))

        return prazna_susedna_polja, puna_susedna_polja
    else:
        return [], []  # Dodajte ovaj red kako biste osigurali da uvek vraćate tuple


def bresenham_line(startRow, startCol, endRow, endCol):
    path = []
    # Parametri za Bresenham algoritam
    dx = abs(endCol - startCol)
    dy = abs(endRow - startRow)
    x, y = startCol, startRow
    sx = 1 if startCol < endCol else -1
    sy = 1 if startRow < endRow else -1
    err = dx - dy
    # Dodajemo početnu tačku
    path.append((y, x))
    # Generisanje linije
    while x != endCol or y != endRow:
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
        # Dodajemo trenutnu tačku u putanju
        path.append((y, x))
    return path
def calculate_diagonal_steps(startRow, startCol, targetRow, targetCol):
    # Funkcija koja računa minimalan broj dijagonalnih koraka između dva polja
    row_distance = abs(targetRow - startRow)
    col_distance = abs(targetCol - startCol)
    return max(row_distance, col_distance)

def find_stacks_at_min_steps(board, startRow, startCol):
  if(board[startRow][startCol]):
    visited = set()
    queue = deque([(startRow, startCol, 0)])  # Torka (row, col, steps)
    min_steps = float('inf')  # Postavljanje početne vrednosti na beskonačno

    while queue:
        row, col, steps = queue.popleft()
        if (row, col) in visited:
            continue

        visited.add((row, col))
        if board[row][col] and row != startRow and col != startCol:
            min_steps = min(min_steps, steps)

        # Dodajemo susedna polja u red za pretragu
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                queue.append((new_row, new_col, steps + 1))

    nearest_stacks = set()

    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col]:
                steps = calculate_diagonal_steps(startRow, startCol, row, col)
                if steps == min_steps:
                    nearest_stacks.add((row, col))

    for stack in nearest_stacks:
        print("Najblizi stek:"+str(stack))
    return list(nearest_stacks)
  else:
      return []
def contains_path_to_nearest_stacks(board, startRow, startCol, endRow, endCol):
    nearest_stacks = find_stacks_at_min_steps(board, startRow, startCol)
    for stack in nearest_stacks:
        path = list(bresenham_line(startRow, startCol, stack[0], stack[1]))
        if (endRow, endCol) in path or path == (endRow ,endCol):
            print("Putanja do najbližeg sadrži ovo polje")
            return True
    return False

def can_reach_diagonal_path(startRow, startCol, targetRow, targetCol, board):
    deltaRow = targetRow - startRow
    deltaCol = targetCol - startCol
    rowStep = 1 if deltaRow > 0 else -1
    colStep = 1 if deltaCol > 0 else -1

    currentRow, currentCol = startRow, startCol

    while currentRow != targetRow or currentCol != targetCol:
        # Provera da li je polje slobodno
        if board[currentRow][currentCol]:
            return False
        # Pomeranje na sledeće polje
        currentRow += rowStep
        currentCol += colStep

    # Ako se uspešno došlo do cilja po dijagonali, vraćamo True
    return True





def IsValidMove(board, startRow, startCol, endRow, endCol, start, image1, image2, n,brojac,index):
    prazna,puna=get_diagonal_neighbors(board,startRow,startCol)
    if (
            board[startRow][startCol]
            and ((start and board[startRow][startCol][0].color == image2.color) or (not start))
            and ((brojac % 2 == 0 and board[startRow][startCol][index].color == image2.color)
                 or (brojac % 2 == 1 and board[startRow][startCol][index].color == image1.color))
            and abs(endRow - startRow) == 1
            and abs(endCol - startCol) == 1
            and (len(board[endRow][endCol]) + len(board[startRow][startCol])-index) < 9
            and (index < len(board[endRow][endCol]) or len(board[endRow][endCol]) == 0)
            and ( (puna != []
                and len(board[endRow][endCol]) != 0) or (puna==[]  and prazna != []))
            and contains_path_to_nearest_stacks(board, startRow, startCol, endRow, endCol)
    ):
        return True
    else:
        return False



def PlayerMove(board, startRow, startCol, endRow, endCol, start, igrac1, igrac2, image1, image2, n,brojac,index):
    # provera da li se potez poklapa sa pravilima



    if (

            IsValidMove(board, startRow, startCol, endRow, endCol, start, image1, image2, n, brojac, index)
    ):

        if(start and board[startRow][startCol][0].color == image2.color ):
                start = False
                print('Start je ' + str(start))

        board[endRow][endCol] += board[startRow][startCol][index:]
        # Izbriši figure sa steka
        del board[startRow][startCol][index:]
        brojac+=1
        print('Trenutno na steku ' + str(len(board[endRow][endCol])))
        if len(board[endRow][endCol]) == 8:
            if board[endRow][endCol][7].color == image1.color:
                print(board[endRow][endCol])
                igrac1 += 1
                if igrac1 == (((n - 2) * n) // 32) + 1:
                    print('Igra zavrsena. Igrac 1 pobedio!')
                    return start, igrac1, igrac2, False,brojac

                print('Igrac 1:  ' + str(igrac1))
                print('Igrac 2: ' + str(igrac2))
            elif board[endRow][endCol][7].color == image2.color:
                print(board[endRow][endCol])
                igrac2 += 1
                print('Igrac 2: ' + str(igrac2))
                print('Igrac 1: ' + str(igrac1))
                if igrac2 == (((n - 2) * n) // 32) + 1:
                    print('Igra zavrsena. Igrac 2 pobedio!')
                    return start, igrac1, igrac2, False,brojac

            board[endRow][endCol].clear()

    return start, igrac1, igrac2, True,brojac

def draw_game_state(screen, board, cell_size, n, sqSelected):
    # Ispisivanje table
    screen.fill((255, 255, 255))
    draw_board(screen, cell_size, n)
    draw_labels(screen, cell_size, n)

    # Ispisivanje figura na tabli
    for row in range(n):
        for col in range(n):
            pieces = board[row][col]
            if pieces:
                     # Ako je lista slika, iscrtajte svaku odvojeno
                    for i, piece in enumerate(pieces):
                        offset = i*13.5214
                        screen.blit(piece.original_image, (col * cell_size + 5, row * cell_size + 5- offset))

    # Ispisivanje selektovane pozicije, ako postoji
    if sqSelected:
        pygame.draw.rect(screen, (0, 255, 0),
                         (sqSelected[1] * cell_size, sqSelected[0] * cell_size, cell_size, cell_size), 3)

    pygame.display.flip()
def game_loop(screen,selected_color, board, cell_size, n, image1, image2):
    running = True
    sqSelected = None  # Postavljamo na None umesto praznog tuple-a
    playerClicks = []
    start = True
    igrac1 = 0
    igrac2 = 0
    brojac=0
    show_dialog = True
    index=int

    while running:
        time.sleep(0.15)
        if((selected_color=='WHITE' and brojac%2==0) or (selected_color=='BLACK' and brojac %2 ==1)):
            if(selected_color=='WHITE'):
                evaluated_dict = evaluate_state(board, image2.color)
            else:
                evaluated_dict = evaluate_state(board,image1.color)
            max_entries = find_max_entries(evaluated_dict)

            # Provera da li postoje maksimalni unosi
            if max_entries:
                # Uzimanje prvog maksimalnog unosa
                ((startrow, startcol, index), data) = max_entries[0]

                # Uzimanje ključeva iz data
                keys = list(data.keys())

                # Uzimanje vrednosti ključeva
                (endrow, endcol) = keys[0]

                # Ispis vrednosti promenljivih
                print(f"startrow: {startrow}")
                print(f"startcol: {startcol}")
                print(f"index: {index}")
                print(f"endrow: {endrow}")
                print(f"endcol: {endcol}")
                start, igrac1, igrac2, running, brojac = PlayerMove(board, startrow, startcol, endrow, endcol,
                                                                    start, igrac1,
                                                                    igrac2, image1, image2, n, brojac, index)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:

                row = event.pos[1] // cell_size
                col = event.pos[0] // cell_size


                if sqSelected == (row, col):
                    sqSelected = None  # Ako ponovo kliknemo na istu figuru, odselektujemo je
                    playerClicks = []
                elif not playerClicks:
                    print('Brojac je '+str(brojac))
                    if (brojac % 2 == 0):
                        color = image2.color
                    else:
                        color = image1.color
                    good = GoodMoves(board, color)

                    if (good == {}):
                        brojac += 1
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                    get_diagonal_neighbors(board,row,col)
                    find_stacks_at_min_steps(board,row,col)

                    show_dialog = True
                    index=0
                    if board[sqSelected[0]][sqSelected[1]]:
                        index =show_selected_piece_window(sqSelected, board, screen, cell_size)
                     #new_states(good,row,col,ind)
                    evaluate_state(board, color)
                    find_max_entries(evaluate_state(board,color))
                    find_min_entries(evaluate_state(board,color))
                    # max_stanje(board, color, row, col, index)
                elif playerClicks:

                    startRow, startCol = playerClicks[0]
                    endRow, endCol = (row, col)


                    start, igrac1, igrac2, running, brojac = PlayerMove(board, startRow, startCol, endRow, endCol,
                                                                            start, igrac1,
                                                                            igrac2, image1, image2, n, brojac, index)


                    sqSelected = None  # Resetuj selekciju
                    playerClicks = []
                    show_dialog = False

        # if show_dialog and sqSelected is not None and board[sqSelected[0]][sqSelected[1]]:
        #
        #     draw_game_state(screen, board, cell_size, n, sqSelected)
        #
        #     show_dialog = False
        # else:
            draw_game_state(screen, board, cell_size, n, sqSelected)

    pygame.quit()
    sys.exit()


def main():
    initialize()
    screen = setup_window()
    selected_color = choose_color_dialog()
    igrac1 = 0
    igrac2 = 0
    selected_size = choose_board_size_dialog()
    cell_size = setup_window().get_width() // selected_size
    image1, image2 = load_and_resize_images(cell_size)
    print(image1)

    if selected_size:
        n = selected_size
        board = create_board(cell_size, n)
        print(str((n-2)*n//32+1))
        game_loop(screen,selected_color, board, cell_size, n,image1,image2)

if __name__ == "__main__":
    main()