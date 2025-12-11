
import pygame
import sys
import config
import algorithms

class Button:
    """A simple clickable button class."""
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen, font, is_active=False):
        draw_color = self.hover_color if self.is_hovered else self.color
        if is_active:
            draw_color = config.TAB_ACTIVE_COLOR
        
        pygame.draw.rect(screen, draw_color, self.rect)
        text_surf = font.render(self.text, True, config.BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered

class VisualizerState:
    """Holds the state for a single sorting algorithm instance."""
    def __init__(self, sort_type):
        self.sort_type = sort_type
        self.accent_color = self.get_accent_color()
        self.reset()

    def get_accent_color(self):
        if self.sort_type == 'cascade': return config.CASCADE_COLOR
        if self.sort_type == 'pigeonhole': return config.PIGEONHOLE_COLOR
        return config.BALANCE_BEAM_SWAP_COLOR

    def reset(self):
        self.data, self.max_val = algorithms.generate_data(self.sort_type)
        
        # Adjust NUM_BARS for Pigeonhole if its element count is different
        num_elements = len(self.data)
        self.num_bars = config.NUM_BARS if self.sort_type != 'pigeonhole' else num_elements
        
        self.sample_indices = [int(i * (num_elements / self.num_bars)) for i in range(self.num_bars)]
        
        sort_function = getattr(algorithms, f"{self.sort_type}_sort")
        self.generator = sort_function(self.data)
        self.is_sorting = True
        self.start_time = pygame.time.get_ticks()
        self.total_time = 0

class App:
    """The main application class."""
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, config.FONT_SIZE)
        self.big_font = pygame.font.Font(None, 50)
        self.clock = pygame.time.Clock()
        self.app_state = "menu" # "menu" or "visualizer"
        
        self.sorters = {
            "cascade": VisualizerState("cascade"),
            "pigeonhole": VisualizerState("pigeonhole"),
            "balance": VisualizerState("balance"),
        }
        self.active_sorter_name = "cascade"
        
        self.start_button = Button(
            config.SCREEN_WIDTH / 2 - 100, config.SCREEN_HEIGHT / 2 - 25, 
            200, 50, "Start Visualizer", config.BUTTON_COLOR, config.BUTTON_HOVER_COLOR
        )
        self.setup_ui_buttons()

    def setup_ui_buttons(self):
        self.tabs = [
            Button(20, 20, 150, 30, "Cascade Sort", config.TAB_INACTIVE_COLOR, config.BUTTON_HOVER_COLOR),
            Button(180, 20, 150, 30, "Pigeonhole Sort", config.TAB_INACTIVE_COLOR, config.BUTTON_HOVER_COLOR),
            Button(340, 20, 150, 30, "Balance Beam", config.TAB_INACTIVE_COLOR, config.BUTTON_HOVER_COLOR),
        ]
        self.reset_button = Button(config.SCREEN_WIDTH - 120, 20, 100, 30, "Reset", config.BUTTON_COLOR, config.BUTTON_HOVER_COLOR)

    def run(self):
        while True:
            if self.app_state == "menu":
                self.run_menu()
            elif self.app_state == "visualizer":
                self.run_visualizer()

    def run_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.start_button.is_clicked(event):
                self.app_state = "visualizer"
                return

        self.screen.fill(config.BG_COLOR)
        title_surf = self.big_font.render("Sorting Algorithm Visualizer", True, config.FONT_COLOR)
        title_rect = title_surf.get_rect(center=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/3))
        self.screen.blit(title_surf, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        self.start_button.check_hover(mouse_pos)
        self.start_button.draw(self.screen, self.font)
        
        pygame.display.flip()

    def run_visualizer(self):
        sorter = self.sorters[self.active_sorter_name]

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.handle_ui_clicks(event)

        # Update sorting state if active
        if sorter.is_sorting:
            try:
                active_indices, scan_indices = next(sorter.generator)
            except StopIteration:
                sorter.is_sorting = False
                sorter.total_time = (pygame.time.get_ticks() - sorter.start_time) / 1000.0
                print(f"{sorter.sort_type.title()} Sort finished in {sorter.total_time:.4f} seconds.")
                active_indices, scan_indices = set(), set()
        else:
            active_indices, scan_indices = set(), set()

        # Drawing
        self.draw_visualizer_screen(sorter, active_indices, scan_indices)
        pygame.display.flip()
        self.clock.tick(60)

    def handle_ui_clicks(self, event):
        if self.tabs[0].is_clicked(event): self.active_sorter_name = "cascade"
        elif self.tabs[1].is_clicked(event): self.active_sorter_name = "pigeonhole"
        elif self.tabs[2].is_clicked(event): self.active_sorter_name = "balance"
        elif self.reset_button.is_clicked(event):
            self.sorters[self.active_sorter_name].reset()

    def draw_visualizer_screen(self, sorter, active_indices, scan_indices):
        self.screen.fill(config.BG_COLOR)
        self.draw_bars(sorter, active_indices, scan_indices)
        self.draw_ui_overlay(sorter)

    def draw_ui_overlay(self, sorter):
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw tabs
        if self.active_sorter_name == "cascade": self.tabs[0].draw(self.screen, self.font, is_active=True)
        else: self.tabs[0].draw(self.screen, self.font)
        
        if self.active_sorter_name == "pigeonhole": self.tabs[1].draw(self.screen, self.font, is_active=True)
        else: self.tabs[1].draw(self.screen, self.font)
        
        if self.active_sorter_name == "balance": self.tabs[2].draw(self.screen, self.font, is_active=True)
        else: self.tabs[2].draw(self.screen, self.font)

        # Draw reset button
        self.reset_button.draw(self.screen, self.font)

        # Check hovers
        for tab in self.tabs: tab.check_hover(mouse_pos)
        self.reset_button.check_hover(mouse_pos)

        # Draw status text
        if sorter.is_sorting:
            status_text = f"Sorting with {sorter.sort_type.replace('_', ' ').title()} Sort..."
        else:
            status_text = f"Finished! Time: {sorter.total_time:.4f}s"
        text_surf = self.font.render(status_text, True, config.FONT_COLOR)
        self.screen.blit(text_surf, (20, config.SCREEN_HEIGHT - 30))

    def draw_bars(self, sorter, active_indices, scan_indices):
        bar_width = config.SCREEN_WIDTH / sorter.num_bars
        is_line_mode = bar_width < 1.5

        ratio = len(sorter.data) / sorter.num_bars
        active_bars = {int(idx / ratio) for idx in active_indices}
        scan_bars = {int(idx / ratio) for idx in scan_indices}

        for i in range(sorter.num_bars):
            data_idx = sorter.sample_indices[i]
            val = sorter.data[data_idx]
            bar_height = (val / sorter.max_val) * (config.SCREEN_HEIGHT - 80) # Make space for UI
            x = i * bar_width
            y = config.SCREEN_HEIGHT - bar_height

            color = config.BAR_COLOR
            if i in active_bars:
                color = sorter.accent_color
            elif i in scan_bars:
                color = config.BALANCE_BEAM_SCAN_COLOR # Scan color is consistent

            if is_line_mode:
                pygame.draw.line(self.screen, color, (x, y), (x, config.SCREEN_HEIGHT))
            else:
                pygame.draw.rect(self.screen, color, (x, y, bar_width - 1, bar_height))

if __name__ == "__main__":
    app = App()
    app.run()
