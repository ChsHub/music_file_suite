from tkinter import TOP, LEFT

from standard_button import StandardButton
from standard_frame import StandardFrame
from standard_label import StandardLabel
from colors import color_background
from texts import text_preview_details, text_preview_change, text_preview_playlist
class Preview(StandardFrame):


    def __init__(self, master, data, apply_change_callback):
        super().__init__(master, side=TOP)
        preview_frame1 = StandardFrame(self, TOP, borderwidth=1)
        preview_frame = StandardFrame(preview_frame1, TOP, pady=0)

        for x in range(len(text_preview_details)):

            frame = StandardFrame(preview_frame, LEFT, 2, 0)

            StandardLabel(text_preview_details[x], frame, 0, 0, color_background).pack(expand=True, fill='both')

            for y in range(len(data)):
                StandardLabel(data[y][x], frame, 0, 0, color_background).pack(expand=True, fill='both')
                if y == 15:
                    break

        button_frame = StandardFrame(preview_frame1, side=TOP, padx=0, pady=0)
        left_button_frame = StandardFrame(button_frame, side=LEFT, padx=0, pady=0)
        right_button_frame = StandardFrame(button_frame, side=LEFT, padx=0, pady=0)
        StandardButton(text_preview_change, left_button_frame, apply_change_callback, 0, 0).pack(side=TOP)
        StandardButton(text_preview_playlist, right_button_frame, None, 0, 0).pack(side=TOP)
