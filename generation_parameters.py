class GenerationParameters:
    def __init__(self, target_width, target_height, mm_per_pixel, margin_width, margin_height):
        self.target_width = target_width
        self.target_height = target_height
        self.mm_per_pixel = mm_per_pixel

        self.margin_width = margin_width
        self.margin_height = margin_height