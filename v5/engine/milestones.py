import pygame
from config import BUILDINGS
from engine.game_state import GameState


MILESTONES = [
    {
        "id": "gold_100",
        "message": "Premiers pas: +50 gold",
        "condition": lambda state: state.gold >= 100,
        "reward": lambda state: setattr(state, "gold", state.gold + 50)
    },
    {
        "id": "houses_5",
        "message": "Quartier résidentiel : la population grandit",
        "condition": lambda state: state.grid.count_buildings("house") >= 5,
        "reward": lambda state: setattr(state, "population",
                                        state.population + 2)
    },
    {
        "id": "factories_5",
        "message": "Ville active : +100 gold",
        "condition": lambda state: state.grid.count_buildings("factory") >= 5,
        "reward": lambda state: setattr(state, "gold",
                                        state.gold + 100)
    },
    {
        "id": "garden_1",
        "message": "Un jardin apporte de la sérénit´",
        "condition": lambda state: state.grid.count_buildings("garden") >= 1,
        "reward": lambda state: setattr(state, "population",
                                        state.population + 3)
    },
    {
        "id": "harmony_70_time",
        "message": "Ville paisible : la sérénité s'installe",
        "condition": lambda state: state.harmony_time >= 30,
        "reward": lambda state: setattr(state, "population",
                                        state.population + 5)
    },
    {
        "id": "zen_mastery",
        "message": "Maitrise zen : la prospérité s'installe",
        "condition": lambda state: state.harmony_80_time >= 60,
        "reward": lambda state: setattr(state, "gold",
                                        state.gold + 200)
    }
]


class MilestoneSystem:
    def __init__(self) -> None:
        self.popup_timer = 0.0
        self.popup_message = ""

    def check(self, state: GameState) -> None:
        for milestone in MILESTONES:
            if milestone["id"] in state.completed_milestones:
                continue

            if milestone["condition"](state):
                milestone["reward"](state)

                state.completed_milestones.add(milestone["id"])

                self.popup_message = milestone["message"]
                self.popup_timer = 2.5

                print(f"🏆 Milestone unblocked: {milestone['message']}")

    def update(self, dt: float) -> None:
        if self.popup_timer > 0:
            self.popup_timer -= dt
            if self.popup_timer < 0:
                self.popup_timer = 0

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        if self.popup_timer <= 0:
            return

        text = font.render(self.popup_message, True, (255, 255, 100))

        text_rect = text.get_rect(centerx=surface.get_width() // 2, y=150)
        surface.blit(text, text_rect)
