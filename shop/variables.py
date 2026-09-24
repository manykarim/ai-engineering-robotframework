"""Robot Framework variable file: ${SHOP_URL}, ${SHOP_SPACE} and ${SHOP_PROFILE}.

Loaded for every run through robot.toml. It only resolves the values: a
variable file cannot stop a run, so ``shop/preflight.py`` does that.
"""
from shop.config import load


def get_variables():
    settings = load()
    return {"SHOP_URL": settings.url, "SHOP_SPACE": settings.space, "SHOP_PROFILE": settings.profile}
