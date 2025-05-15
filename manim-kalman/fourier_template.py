from manim import *
import numpy as np

class FourierSum(Scene):
    def construct(self):
        # Setup des axes
        axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True}
        ).to_edge(DOWN)

        # Première sinusoïde
        sine1 = axes.plot(lambda x: np.sin(x), color=BLUE)
        label1 = axes.get_graph_label(sine1, label="\\sin(x)", x_val=PI, direction=UP)

        # Deuxième sinusoïde (harmonique)
        sine2 = axes.plot(lambda x: 0.5 * np.sin(2 * x), color=RED)
        label2 = axes.get_graph_label(sine2, label="0.5\\sin(2x)", x_val=PI, direction=UP)

        # Somme des deux sinusoïdes
        sum_curve = axes.plot(lambda x: np.sin(x) + 0.5 * np.sin(2 * x), color=GREEN)
        label_sum = axes.get_graph_label(sum_curve, label="f(x)", x_val=PI, direction=UP)

        # Animation
        self.play(Create(axes))
        self.play(Create(sine1), Write(label1))
        self.play(Create(sine2), Write(label2))
        self.wait(0.5)
        self.play(Create(sum_curve), Write(label_sum))
        self.wait(2)
