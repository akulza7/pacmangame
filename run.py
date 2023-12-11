import json
import pygame
import datetime
from class_area.Area import Area
from class_pacman.pacman import Pacman
from class_ghost.Ghost import Ghost
from class_text.Text import Text, RecalculableText
from class_button.Button import Button
from class_music.Music import Music
from class_healthbar.Healthbar import Healthbar

class Settings:
    scene_changed = True
    """ 
    Индексы сцен:
        0 — Главное меню
        1 — Таблица лидеров
        2 — Старт-экран
        3 — Игра
        4 — Смерть Пакмана
        5 — Game over 
        6 — Победа (съедены все зерна)
    """
    scene_index = 0

def main():
    pygame.init()
    pygame.font.init()

    size = width, height = 945, 900
    color = (0, 0, 0)
    screen = pygame.display.set_mode(size)
    direction = None
    score = None
    gameover = False
    Scaremode_global = {
        "statement": False,
        "start_time": None,
        "seconds": None
    }
    leaders = []
    with open('class_text/records.txt', 'r') as fr:
        leaders = json.load(fr)

    crop_regions = None
    with open('class_ghost/crop_regions.txt', 'r') as fr:
        crop_regions = json.load(fr)

    healthbar = Healthbar()
    player = Music()
    area = Area()
    pacman = Pacman()
    ghosts = [
    Ghost([8, 6], crop_regions["red"]),
    Ghost([9, 6], crop_regions["orange"]),
    Ghost([11, 6], crop_regions["pink"]),
    Ghost([12,6], crop_regions["blue"])
    ] 
    buttons = [
    Button(300, 350, 300, 100, "Play", lambda var=None: startgame(player, area, pacman, healthbar, True)), 
    Button(300, 500, 300, 100, "Highscores", lambda var=None: set_scene(1)),
    Button(300, 650, 300, 100, "Exit", exit)
    ]

    
    
    
    name_text = Text([270,180], "Pacman", 100, (0, 0, 255))
    leaderboard_text = Text([180,180], "Hall of fame", 80, (232, 155, 0))
    highscores = [
        RecalculableText([288, 325], "Top 1: {}", 60, (255, 255, 255)),
        RecalculableText([288, 475], "Top 2: {}", 60, (255, 255, 255)),
        RecalculableText([288, 625], "Top 3: {}", 60, (255, 255, 255))
    ]
    ready_text = Text([415, 360], "Ready!", 36, (255, 255, 0))
    score_text = RecalculableText([45, 4], "Score: {}", 36, (255, 255, 255))
    gameover_text = Text([375, 360], "Game over", 36, (255, 0, 0))

    while not gameover:
        if Settings.scene_changed:
            Settings.scene_changed = False
            if Settings.scene_index == 0:
                score = menu_scene_activation(player)
            if Settings.scene_index == 2:
                start_time, direction, Scaremode_global = start_scene_activation(datetime.datetime.now(), score, score_text, pacman, ghosts, Scaremode_global)
            if Settings.scene_index == 1:
                leaders = leaderboard_activation(highscores)
            if Settings.scene_index == 4:
                death_start_time = death_scene_activation(datetime.datetime.now(), pacman, healthbar)
            if Settings.scene_index == 5:
                gameover_start_time = gameover_scene_activation(datetime.datetime.now(), leaders, score)
            if Settings.scene_index == 6:
                win_start_time = win_scene_activation(datetime.datetime.now())

        if not Settings.scene_changed:
            for event in pygame.event.get():
                gameover = application_process_exit(event)
                if Settings.scene_index == 0:
                    menu_scene_process_event(event, buttons)
                if Settings.scene_index == 1:
                    leaderboard_scene_process_event(event)
                if Settings.scene_index == 2:
                    direction = start_scene_process_event(event, direction)
                if Settings.scene_index == 3:
                    direction = game_scene_process_event(event, direction)

        if not Settings.scene_changed:
            if Settings.scene_index == 2:
                timer_process_logic(start_time, max_wait_seconds=3, scene_index=3)
            if Settings.scene_index == 6:
                win_timer_process_logic(win_start_time, max_wait_seconds=3, area=area, pacman=pacman, healthbar=healthbar)
            if Settings.scene_index == 5:
                timer_process_logic(gameover_start_time, max_wait_seconds=3, scene_index=0)
            if Settings.scene_index == 4:
                timer_process_logic(death_start_time, max_wait_seconds=3, scene_index=is_alive(pacman))
            if Settings.scene_index == 3:
                score = game_scene_process_logic(area, pacman, 
                ghosts, direction, score_text, score, Scaremode_global)

        if not Settings.scene_changed:
            screen.fill(color)
            if Settings.scene_index == 0:
                menu_scene_process_draw(screen, name_text, buttons)
            if Settings.scene_index == 1:
                leaderboard_process_draw(screen, highscores, leaderboard_text)
            if Settings.scene_index > 1:
                game_stage_draw(screen, area, pacman, ghosts, score_text, healthbar)
            if Settings.scene_index == 2:
                plaintext_draw(screen, ready_text)
            if Settings.scene_index == 5:
                gameover_scene_draw(screen, area, score_text, gameover_text)
            pygame.display.flip()
            pygame.time.wait(20)
    return

def application_process_exit(event):
    if event.type == pygame.QUIT:
        return True
    else:
        return False

def startgame(player, area, pacman, healthbar, newgame=True):
    if newgame == True:
        player.play()
        pacman.set_health(3)
        healthbar.reset()
    with open('class_area/map.txt', 'r') as fr:
        area.updateMap(json.load(fr))
    set_scene(2)

def is_alive(pacman):
    return 2 if pacman.get_health()>0 else 5

def menu_scene_activation(player):
    player.stop()
    score = 0
    return score

def start_scene_activation(start_time, score, score_text, pacman, ghosts, SCAREMODE):
    score_text.recreate_text(score)
    pacman.respawn([450,450], [10,10])
    direction = "left"
    SCAREMODE["statement"] = False
    for ghost in ghosts:
        ghost.respawn()
    return start_time, direction, SCAREMODE

def leaderboard_activation(highscores):
    leaders = []
    with open('class_text/records.txt', 'r') as fr:
        leaders = json.load(fr)
    for i in range(3):
        highscores[i].recreate_text(leaders[i])
    return leaders

def death_scene_activation(start_time, pacman, healthbar):
    pacman.set_health(pacman.get_health()-1)
    healthbar.decrease()
    return start_time

def gameover_scene_activation(start_time, leaders, score):
    update_leaderboard(leaders, score)
    return start_time

def win_scene_activation(start_time):
    return start_time

def menu_scene_process_event(event, buttons):
    for button in buttons:
        button.event(event)

def leaderboard_scene_process_event(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        Settings.scene_changed = True
        Settings.scene_index = 0

def start_scene_process_event(event, direction):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            direction = "down"
        if event.key == pygame.K_w:
            direction = "up"
        if event.key == pygame.K_a:
            direction = "left"
        if event.key == pygame.K_d:
            direction = "right"
    return direction

def game_scene_process_event(event, direction):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            direction = "down"
        if event.key == pygame.K_w:
            direction = "up"
        if event.key == pygame.K_a:
            direction = "left"
        if event.key == pygame.K_d:
            direction = "right"
    return direction

def game_scene_process_logic(area, pacman, ghosts, direction, score_text, score, SCAREMODE):
    if(SCAREMODE["statement"] == True):
        SCAREMODE["statement"], SCAREMODE["seconds"] = scaremode_timer_process_logic(SCAREMODE["start_time"])
    deltascore, scaremode, newmap = \
        pacman.logic(map=area.map, ghosts=ghosts, scaremode_status=SCAREMODE["statement"], direction=direction)
    area.updateMap(newmap)
    if scaremode == True:
        SCAREMODE["statement"] = True
        SCAREMODE["start_time"] = datetime.datetime.now()
        SCAREMODE["seconds"] = 0
    if deltascore < 0:
        set_scene(4)
    else:
        score += deltascore
        score_text.recreate_text(score)
    for ghost in ghosts:
        ghost.logic(scaremode, SCAREMODE["statement"], area.map, SCAREMODE["seconds"])
    if area.check_corns() == True: 
        set_scene(6)
    return score


def timer_process_logic(start_time, max_wait_seconds, scene_index):
    now = datetime.datetime.now()
    wait_seconds = (now - start_time).seconds
    if wait_seconds == max_wait_seconds:
        set_scene(scene_index)

def scaremode_timer_process_logic(scaremode_start_time):
    now = datetime.datetime.now()
    seconds = (now - scaremode_start_time).seconds
    if seconds == 7:
        return False, None
    else:
        return True, seconds

def win_timer_process_logic(start_time, max_wait_seconds, area, pacman, healthbar):
    now = datetime.datetime.now()
    seconds = (now - start_time).seconds
    if seconds == max_wait_seconds:
        startgame(None, area, pacman, healthbar, False)

def update_leaderboard(leaders, score):
    if score > leaders[0]:
        leaders = [score]+leaders[:2]
    elif score > leaders[1]:
        leaders = leaders[:1]+[score]+leaders[1:2]
    elif score > leaders[2]:
        leaders = leaders[:2]+[score]
    leaders.sort(reverse = True)
    with open('class_text/records.txt', 'w') as fw:
        json.dump(leaders, fw)   

def menu_scene_process_draw(screen, name_text, buttons):
    plaintext_draw(screen, name_text)
    for button in buttons:
        button.draw(screen)

def leaderboard_process_draw(screen, highscores, leaderboard_text):
    plaintext_draw(screen, leaderboard_text)
    for highscoretext in highscores:
        highscoretext.draw(screen)

def game_stage_draw(screen, area, pacman, ghosts, score_text, healthbar):
    area.draw(screen)
    pacman.draw(screen)
    for ghost in ghosts:
        ghost.draw(screen)
    score_text.draw(screen)
    healthbar.draw(screen)

def gameover_scene_draw(screen, area, score_text, gameover_text):
    area.draw(screen)
    score_text.draw(screen) 
    plaintext_draw(screen, gameover_text)  

def plaintext_draw(screen, text):
    text.render()
    text.draw(screen)

def set_scene(index):
    Settings.scene_changed = True
    Settings.scene_index = index


if __name__ == '__main__':
    main()