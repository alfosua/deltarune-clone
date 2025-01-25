from engine.resources.resolution import asset

def sprite(name: str):
    return asset(f"sprites/{name}.json")

LINKLE_IDLE = sprite("charas/linkle-idle")
