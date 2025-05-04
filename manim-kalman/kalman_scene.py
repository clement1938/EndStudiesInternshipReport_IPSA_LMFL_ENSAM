from manim import *
import numpy as np

class KalmanParticles(Scene):
    def construct(self):
        # === Fond de grille ===
        plane = NumberPlane(
            x_range=[-5, 5],
            y_range=[-3, 3],
            background_line_style={"stroke_opacity": 0.4}
        )
        self.add(plane)

        # === Ensemble initial (50 particules) ===
        np.random.seed(42)  # Pour des résultats reproductibles
        particles = VGroup(*[
            Dot(point=[np.random.normal(0, 0.5), np.random.normal(0, 0.5), 0],
                radius=0.05, color=BLUE)
            for _ in range(50)
        ])
        self.play(FadeIn(particles), run_time=1)

        # === Moyenne initiale ===
        def compute_mean(particle_group):
            points = np.array([p.get_center()[:2] for p in particle_group])
            return np.mean(points, axis=0)

        mean_pos = compute_mean(particles)
        mean_dot = Dot(point=np.append(mean_pos, 0), color=GREEN, radius=0.08)
        mean_label = Text("Moyenne", color=GREEN).scale(0.4).next_to(mean_dot, DOWN)
        self.play(FadeIn(mean_dot), FadeIn(mean_label))

        # === Texte "Prévision" ===
        forecast_text = Text("Prévision").scale(0.5).to_corner(UL)
        self.play(Write(forecast_text))

        # === Déplacement (étape de prévision) ===
        forecast_shift = RIGHT * 2 + UP * 0.5
        self.play(particles.animate.shift(forecast_shift), run_time=2)

        # Mise à jour du point moyen
        new_mean = compute_mean(particles)
        self.play(mean_dot.animate.move_to(np.append(new_mean, 0)), run_time=1)
        self.wait(0.5)

        # === Observation (point rouge) ===
        observation = Dot(point=[1.5, 1, 0], color=RED)
        obs_label = Text("Observation", color=RED).scale(0.4).next_to(observation, RIGHT)
        self.play(FadeIn(observation), FadeIn(obs_label), run_time=1)

        # === Vecteurs d’erreur ===
        arrows = VGroup()
        for p in particles:
            arrow = Arrow(start=p.get_center(), end=observation.get_center(), buff=0.05, stroke_width=1)
            arrows.add(arrow)
        self.play(Create(arrows), run_time=2)
        self.wait()

        # === Texte "Correction" ===
        correction_text = Text("Correction").scale(0.5).next_to(forecast_text, DOWN)
        self.play(Write(correction_text))

        # === Correction : déplacement des particules vers l’observation ===
        self.play(*[
            p.animate.move_to(p.get_center() + 0.5 * (observation.get_center() - p.get_center()))
            for p in particles
        ], run_time=2)

        # Mise à jour du point moyen après correction
        corrected_mean = compute_mean(particles)
        self.play(mean_dot.animate.move_to(np.append(corrected_mean, 0)), run_time=1)

        self.wait()
