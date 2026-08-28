import pygame
import random
import json
import os


pygame.init()


# 視窗大小
screen_width = 720
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
fps = pygame.time.Clock()


# font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)
bg_font = pygame.font.Font(None, 250)
titleFont = pygame.font.Font(None, 32)


# 冒泡排序


def save_score(name, score):
   file_path = "leaderboard.json"
   if os.path.exists(file_path):
       with open(file_path, "r") as f:
           data = json.load(f)
   else:
       data = []


   data.append({"name": name, "score": score})


   n = len(data)
   for i in range(n):
       for j in range(0, n - i - 1):
           if data[j]["score"] < data[j + 1]["score"]:
               data[j], data[j + 1] = data[j + 1], data[j]


   with open(file_path, "w") as f:
       json.dump(data[:10], f)




def load_leaderboard():
   if os.path.exists("leaderboard.json"):
       with open("leaderboard.json", "r") as f:
           return json.load(f)
   return []


# 有效性檢驗


def start_panel(game_state, player_name, running):
   screen.fill((0, 0, 0))
   title = titleFont.render("Snake Game", True, (0, 255, 0))
   screen.blit(title, (screen_width // 2 - title.get_width() // 2, 100))


   input_box = pygame.Rect(260, 220, 200, 32)
   pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
   name_text = font.render(player_name, True, (255, 255, 255))
   screen.blit(name_text, (input_box.x + 5, input_box.y + 4))


   hint_text = font.render("Enter your name (max 8 chars):", True, (255, 255, 255))
   screen.blit(hint_text, (screen_width // 2 - hint_text.get_width() // 2, 180))


   btn_rect = pygame.Rect(310, 300, 100, 40)
   pygame.draw.rect(screen, (0, 255, 0), btn_rect)
   btn_text = font.render("Start", True, (0, 0, 0))
   screen.blit(btn_text, (btn_rect.x + 20, btn_rect.y + 8))


   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
       elif event.type == pygame.KEYDOWN:
           if event.key == pygame.K_ESCAPE:
               running = False
           elif event.key == pygame.K_BACKSPACE:
               player_name = player_name[:-1]
           elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and len(player_name) > 0:
               game_state = 'play'
           elif len(player_name) < 8:
               player_name += event.unicode
       elif event.type == pygame.MOUSEBUTTONDOWN:
           if btn_rect.collidepoint(event.pos) and len(player_name) > 0:
               game_state = 'play'


   pygame.display.flip()
   return game_state, player_name, running




def reset_game():
   global snake_head, snake_body, apple_x, apple_y, direction, change_to, score, scored_saved
   snake_head = [100, 100]
   snake_body = [[100, 100], [90, 100], [80, 100]]
   apple_x, apple_y = random.randrange(0, 710, 10), random.randrange(0, 470, 10)
   direction = change_to = 'RIGHT'
   score = 0
   scored_saved = False




# 初始化
reset_game()
game_state = "start"
player_name = ""
running = True


while running:
   if game_state == "start":
       game_state, player_name, running = start_panel(game_state, player_name, running)
       if game_state == "play":
           reset_game()
       fps.tick(30)
       continue


   elif game_state == "leaderboard":
       screen.fill((0, 0, 0))
       lb_title = titleFont.render("Top 10 Leaderboard", True, (0, 255, 0))
       screen.blit(lb_title, (screen_width // 2 - lb_title.get_width() // 2, 50))


       records = load_leaderboard()
       for i, rec in enumerate(records):
           rec_txt = small_font.render(f"{i + 1}. {rec['name']} - {rec['score']}", True, (255, 255, 255))
           screen.blit(rec_txt, (280, 100 + i * 30))


       hint = small_font.render("Press ESC to Menu", True, (255, 255, 255))
       screen.blit(hint, (screen_width // 2 - hint.get_width() // 2, 420))


       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
               game_state = "start"


       pygame.display.flip()
       fps.tick(30)
       continue


   screen.fill((0, 0, 0))


   # 巢式
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_ESCAPE:
               game_state = "start"
           if game_state == "end":
               if event.key == pygame.K_SPACE:
                   reset_game()
                   game_state = "play"
               if event.key == pygame.K_l:
                   game_state = "leaderboard"
           elif game_state == "play":
               if event.key == pygame.K_RIGHT:
                   change_to = 'RIGHT'
               if event.key == pygame.K_LEFT:
                   change_to = 'LEFT'
               if event.key == pygame.K_UP:
                   change_to = 'UP'
               if event.key == pygame.K_DOWN:
                   change_to = 'DOWN'


   if game_state == "play":
       if change_to == 'UP' and direction != 'DOWN': direction = 'UP'
       if change_to == 'DOWN' and direction != 'UP': direction = 'DOWN'
       if change_to == 'LEFT' and direction != 'RIGHT': direction = 'LEFT'
       if change_to == 'RIGHT' and direction != 'LEFT': direction = 'RIGHT'


       if direction == 'UP':
           snake_head[1] -= 10
       elif direction == 'DOWN':
           snake_head[1] += 10
       elif direction == 'LEFT':
           snake_head[0] -= 10
       elif direction == 'RIGHT':
           snake_head[0] += 10


       snake_body.insert(0, list(snake_head))


       # 边界
       if snake_head[0] > 720 or snake_head[0] < 0 or snake_head[1] > 480 or snake_head[1] < 0:
           game_state = "end"


           # 蛇身碰撞
       for i in range(1, len(snake_body) - 1):
           if snake_head == snake_body[i]:
               game_state = "end"


       # 吃到食物
       if snake_head[0] == apple_x and snake_head[1] == apple_y:
           score += 10
           apple_x, apple_y = random.randrange(0, 710, 10), random.randrange(0, 470, 10)
       else:
           snake_body.pop()


   # 繪圖
   bg_text = bg_font.render(f"{score:02}", True, (50, 50, 50))
   screen.blit(bg_text, ((screen_width - bg_text.get_width()) // 2, 120))


   if apple_img:
       screen.blit(apple_img, (apple_x - 5, apple_y - 5))
   else:
       pygame.draw.rect(screen, (0, 255, 0), (apple_x, apple_y, 10, 10))


   for block in snake_body:
       pygame.draw.rect(screen, (255, 0, 0), (block[0], block[1], 10, 10))


   if game_state == "end":
       if not scored_saved:
           save_score(player_name, score)
           scored_saved = True


       gameover_title = titleFont.render("Game Over!", True, (255, 0, 0))
       screen.blit(gameover_title, (screen_width // 2 - gameover_title.get_width() // 2, 120))


       score_text = font.render(f"Score: {score}", True, (255, 255, 255))
       screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 180))


       msgs = ["Press SPACE to Restart", "Press L for Leaderboard", "Press ESC for Menu"]
       for i, m in enumerate(msgs):
           txt = font.render(m, True, (255, 255, 255))
           screen.blit(txt, (screen_width // 2 - txt.get_width() // 2, 240 + i * 40))


   pygame.display.flip()
   fps.tick(30)


pygame.quit()
