import pygame
import random
import os

pygame.init()

print("як я сюди потрапив? Треба вибиратися звідси, може цей ключ допоможе?")

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Втеча з лабіринту')


background_color = (0, 0, 0)
cell_size = 40

wall_img = pygame.image.load('wall.jpg')
wall_img = pygame.transform.scale(wall_img, (cell_size, cell_size))

player_frames = []
for i in range(1, 7):
    fname = f'run{i}.jpg'
    try:
        img = pygame.image.load(fname)
        img = pygame.transform.scale(img, (cell_size, cell_size))
    except Exception:
        
        img = pygame.Surface((cell_size, cell_size))
        img.fill((200 - i * 20, 50 + i * 20, 50))
    player_frames.append(img)


try:
    wall_img = pygame.image.load('wall.jpg')
    wall_img = pygame.transform.scale(wall_img, (cell_size, cell_size))
except Exception:
    wall_img = pygame.Surface((cell_size, cell_size))
    wall_img.fill((100, 100, 100))

try:
    key_img = pygame.image.load('key.png')
    key_img = pygame.transform.scale(key_img, (cell_size, cell_size))
except Exception:
    key_img = pygame.Surface((cell_size, cell_size))
    key_img.fill((255, 215, 0))


coin_img = None
script_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
for name in ('coin.png', 'coin.jpg', 'coin.jpeg'):
    
    p1 = os.path.join(script_dir, name)
    if os.path.exists(p1):
        try:
            coin_img = pygame.image.load(p1)
            coin_img = pygame.transform.scale(coin_img, (cell_size, cell_size))
            break
        except Exception:
            coin_img = None
    
    p2 = os.path.join(parent_dir, name)
    if os.path.exists(p2):
        try:
            coin_img = pygame.image.load(p2)
            coin_img = pygame.transform.scale(coin_img, (cell_size, cell_size))
            break
        except Exception:
            coin_img = None

if coin_img is None:
   
    try:
        coin_img = pygame.image.load('coin.png')
        coin_img = pygame.transform.scale(coin_img, (cell_size, cell_size))
    except Exception:
        coin_img = pygame.Surface((cell_size, cell_size))
        coin_img.fill((255, 223, 0))


coin_sound = None
key_sound = None
bg_music = None
try:
    pygame.mixer.init()
    
    for sname in ('coin_sound.wav', 'coin_sound.ogg'):
        p = os.path.join(script_dir, sname)
        if os.path.exists(p):
            try:
                coin_sound = pygame.mixer.Sound(p)
                break
            except Exception:
                coin_sound = None
        
        p2 = os.path.join(parent_dir, sname)
        if os.path.exists(p2):
            try:
                coin_sound = pygame.mixer.Sound(p2)
                break
            except Exception:
                coin_sound = None
    for sname in ('keys_sound.wav', 'key_sound.wav', 'keys_sound.ogg', 'key_sound.ogg'):
        p = os.path.join(script_dir, sname)
        if os.path.exists(p):
            try:
                key_sound = pygame.mixer.Sound(p)
                break
            except Exception:
                key_sound = None
        p2 = os.path.join(parent_dir, sname)
        if os.path.exists(p2):
            try:
                key_sound = pygame.mixer.Sound(p2)
                break
            except Exception:
                key_sound = None
    
    for mname in ('game_sound.wav', 'game_sound.ogg'):
        p = os.path.join(parent_dir, mname)
        if os.path.exists(p):
            try:
                bg_music = p
                break
            except Exception:
                bg_music = None
   
    if bg_music is not None:
        try:
            pygame.mixer.music.load(bg_music)
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)
        except Exception:
            pass
except Exception:
   
    coin_sound = None
    key_sound = None
    bg_music = None

try:
    door_img = pygame.image.load('door.jpg')
    door_img = pygame.transform.scale(door_img, (cell_size, cell_size))
except Exception:
    door_img = pygame.Surface((cell_size, cell_size))
    door_img.fill((150, 75, 0))


maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


character_position = [200, 200]

free_cells = []
for y in range(len(maze)):
    for x in range(len(maze[y])):
        if maze[y][x] == 0:
            free_cells.append([x, y])


key_position = random.choice(free_cells[:-1])
door_position = free_cells[-1]


available_for_coins = [c for c in free_cells if c != key_position and c != door_position]
coin_positions = []
try:
    
    coin_positions = random.sample(available_for_coins, k=min(3, len(available_for_coins)))
except Exception:
   
    coin_positions = available_for_coins[:3]


possible_starts = [c for c in free_cells if c != key_position and c != door_position]
player_cell = possible_starts[0] if possible_starts else [1, 1]


trap_candidates = [c for c in free_cells if c != key_position and c != door_position and c not in coin_positions]
trap_position = None
if trap_candidates:
   
    start_cell = player_cell
    non_start_candidates = [c for c in trap_candidates if c != start_cell]
    trap_position = random.choice(non_start_candidates or trap_candidates)


trap_triggered = False
trap_visible = False
trapped = False
trapped_end_time = 0


trap_img = pygame.Surface((cell_size, cell_size))
trap_img.fill((200, 0, 0))


moving = False
move_start_px = player_cell[0] * cell_size
move_start_py = player_cell[1] * cell_size
move_target_cell = None
move_progress = 0.0  
move_speed = 8.0  


has_key = False


frame_index = 0
frame_time = 80  
last_frame_update = pygame.time.get_ticks()

clock = pygame.time.Clock()


def show_start_screen():
    showing = True
    font = pygame.font.SysFont('arial', 32)
    small_font = pygame.font.SysFont('arial', 24)
    while showing:
        screen.fill((0, 0, 0))
        title = font.render("Втеча з лабіринту", True, (255, 255, 255))
        how_to = small_font.render("Як грати:", True, (255, 255, 255))
        controls = [
            "W, A, S, D - рухатися",
            "E - взаємодіяти з речами",
            "",
            "Натисни будь-яку клавішу, щоб почати гру"
        ]

        screen.blit(title, (230, 100))
        screen.blit(how_to, (330, 200))
        for i, line in enumerate(controls):
            text = small_font.render(line, True, (200, 200, 200))
            screen.blit(text, (180, 250 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                showing = False


show_start_screen()


running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            
            if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                frame_index = (frame_index + 1) % len(player_frames)
                last_frame_update = pygame.time.get_ticks()

            if not moving and not trapped:
                dx, dy = 0, 0
                if event.key == pygame.K_w:
                    dy = -1
                elif event.key == pygame.K_s:
                    dy = 1
                elif event.key == pygame.K_a:
                    dx = -1
                elif event.key == pygame.K_d:
                    dx = 1

                if dx != 0 or dy != 0:
                    tx = player_cell[0] + dx
                    ty = player_cell[1] + dy

                    if 0 <= ty < len(maze) and 0 <= tx < len(maze[0]) and maze[ty][tx] == 0:
                        moving = True
                        move_target_cell = [tx, ty]
                        move_start_px = player_cell[0] * cell_size
                        move_start_py = player_cell[1] * cell_size
                        move_progress = 0.0

            if event.key == pygame.K_e:
                
                picked_coin = False
                for c in coin_positions:
                    if c == player_cell:
                        coin_positions.remove(c)
                        picked_coin = True
                        print('Coin picked up!')
                        try:
                            if coin_sound is not None:
                                coin_sound.play()
                        except Exception:
                            pass
                        break

                
                if not picked_coin:
                    if key_position is not None and player_cell == key_position and not has_key:
                        has_key = True
                        key_position = None
                        print('Ти підібрав ключ!')
                        try:
                            if key_sound is not None:
                                key_sound.play()
                        except Exception:
                            pass
                    elif has_key and player_cell == door_position:
                        print('Ти вийшов з лабіринта, ти тепер крутий!')
                        running = False
        elif event.type == pygame.KEYUP:
            
            pass

  
    if moving and move_target_cell is not None:
        move_progress += move_speed
       
        ratio = min(move_progress / cell_size, 1.0)
        target_px = move_target_cell[0] * cell_size
        target_py = move_target_cell[1] * cell_size
        cur_px = move_start_px + (target_px - move_start_px) * ratio
        cur_py = move_start_py + (target_py - move_start_py) * ratio
        if ratio >= 1.0:
           
            player_cell = move_target_cell
            moving = False
            move_target_cell = None
            move_progress = 0.0
           

    else:
       
        cur_px = player_cell[0] * cell_size
        cur_py = player_cell[1] * cell_size

    
    if moving:
        now = pygame.time.get_ticks()
        if now - last_frame_update >= frame_time:
            last_frame_update = now
            frame_index = (frame_index + 1) % len(player_frames)

   
    screen.fill(background_color)
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 1:
                screen.blit(wall_img, (x * cell_size, y * cell_size))

    
    if key_position is not None:
        screen.blit(key_img, (key_position[0] * cell_size, key_position[1] * cell_size))
   
    for c in coin_positions:
        screen.blit(coin_img, (c[0] * cell_size, c[1] * cell_size))
    screen.blit(door_img, (door_position[0] * cell_size, door_position[1] * cell_size))

   
    
    player_img = player_frames[frame_index % len(player_frames)]
    screen.blit(player_img, (int(cur_px), int(cur_py)))

    pygame.display.flip()

pygame.quit()