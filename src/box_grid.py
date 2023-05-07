import pygame


class BoxGrid:
    def __init__(self, rows, cols, box_size=50):
        self.rows = rows
        self.cols = cols
        self.box_size = box_size
        self.width = cols * box_size
        self.height = rows * box_size

        self.clicked_boxes = set()
        self.clicked_boxes_list = []

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Box Clicker")

    def draw_boxes(self):
        for row in range(self.rows):
            for col in range(self.cols):
                box_id = f"{row}-{col}"
                color = (0, 0, 255) if box_id in self.clicked_boxes else (255, 255, 255)
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        col * self.box_size,
                        row * self.box_size,
                        self.box_size,
                        self.box_size,
                    ),
                )
                pygame.draw.rect(
                    self.screen,
                    (0, 0, 0),
                    (
                        col * self.box_size,
                        row * self.box_size,
                        self.box_size,
                        self.box_size,
                    ),
                    1,
                )

    def mainloop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    row = y // self.box_size
                    col = x // self.box_size
                    box_id = f"{row}-{col}"
                    if box_id not in self.clicked_boxes:
                        self.clicked_boxes.add(box_id)
                        self.clicked_boxes_list.append((row, col))
                        print(f"Clicked box: {box_id}")
                    else:
                        self.clicked_boxes.remove(box_id)
                        self.clicked_boxes_list.remove((row, col))
                        print(f"Unclicked box: {box_id}")

            self.screen.fill((255, 255, 255))
            self.draw_boxes()
            pygame.display.flip()

        pygame.quit()

    def get_clicked_boxes(self):
        return self.clicked_boxes_list
