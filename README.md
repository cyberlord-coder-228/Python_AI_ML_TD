# Python_AI_ML_TD
Simple Tower Defense game that utilizes AI and ML,
created as a learning project.

How to play:
left mouse click - place turrel (red tower)
middle mouse click - place impulser (green tower)
right mouse click - place bomber (blue tower)

Towers shoot autonomosly. You cannot place more that 4 towers at a time.

If enemy unit reaches your fortress, you lose 1 heart. You have 20 hearts in total.

Computers objective:
Attacker places units (mindless moving missiles) and tries to end the game by destroying your fortress.
Agent uses machine learning to determine the best unit placement and type.

One of four unit types (yellow) is self-improving. It uses generational algorithm to tweak it's parameters for the best unit survival.
