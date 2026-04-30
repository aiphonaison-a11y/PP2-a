# generate_assets.py
import pygame
import os

pygame.init()
WIDTH, HEIGHT = 360, 640

def create_folder():
    os.makedirs("assets/images", exist_ok=True)

def save_image(name, width, height, color, text="", text_color=(255,255,255)):
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Background
    surf.fill(color)
    
    # Border
    pygame.draw.rect(surf, (255,255,255), (0, 0, width, height), 4)
    
    if text:
        font = pygame.font.SysFont("Arial", 18, bold=True)
        txt_surf = font.render(text, True, text_color)
        surf.blit(txt_surf, (width//2 - txt_surf.get_width()//2, height//2 - txt_surf.get_height()//2))
    
    pygame.image.save(surf, f"assets/images/{name}")
    print(f"Created: assets/images/{name}")

create_folder()

# === Create all needed images ===

# Cars
save_image("player_car.png", 70, 120, (0, 100, 255), "YOU", (255,255,255))
save_image("enemy_car.png",  70, 120, (200, 0, 0),   "ENEMY", (255,255,255))

# Coins
save_image("coin.png",       36, 36, (255, 215, 0),   "C", (0,0,0))
save_image("blue_coin.png",  34, 34, (0, 180, 255),   "5", (255,255,255))
save_image("pink_coin.png",  32, 32, (255, 100, 255), "10",(255,255,255))

# Obstacles
save_image("barrier.png",    75, 45, (180, 90, 0),    "BAR", (255,255,255))
save_image("oil.png",        65, 65, (40, 40, 40),    "OIL", (255, 200, 0))

# Power-up / Nitro strip
save_image("speedup.png",    70, 35, (255, 50, 50),   "NITRO", (255,255,255))

print("\n✅ All placeholder images created successfully!")
print("You can now run your game.")