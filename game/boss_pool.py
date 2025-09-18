# game/boss_pool.py
import random

class BossInfo:
    def __init__(self, name: str, portrait: str):
        self.name = name
        self.portrait = portrait

BOSS_POOL = [
    BossInfo("Grimfang der Zermalmer", """
        🐺
       ╱▔▔▔╲
      ( ◣ ◢ )
       ╲_▂_╱
    """),
    BossInfo("Morgrul der Schlächter", """
        🔥👹🔥
       ╭━━━╮
      ( ͡° ͜ʖ ͡°)
       ╰━┳━╯
         👊
    """),
    BossInfo("Elandra die Hexenkönigin", """
        🔮
       (◕‿◕✿)
        ║║║
        ║║║
    """),
    BossInfo("Thorgar der Titan", """
        🪓
       ( •_•)
       /︶︶︶\\
      |   ⚔   |
    """),
    BossInfo("Skarnok der Verrottete", """
        ☠️
       ( x_x)
       /︶︶︶\\
    """),
]

def get_random_boss():
    """Ziehe zufälligen Boss aus dem Pool."""
    return random.choice(BOSS_POOL)
