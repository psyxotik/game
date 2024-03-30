#статистика игры
class Information():
    def __init__(self):
        self.refresh()
        self.run_game = True
        self.cur_music = True
        self.cur_controls = ['K_d', 'K_a']
        with open('dist/data/score.txt', 'r') as f:
            self.hi_score = int(f.readline())

    def refresh(self):
        self.ship_left = 2
        self.score = 0