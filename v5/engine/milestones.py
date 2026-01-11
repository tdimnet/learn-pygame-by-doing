from config import BUILDINGS


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
        pass

    def check(self) -> None:
        pass

    def update(self) -> None:
        pass
