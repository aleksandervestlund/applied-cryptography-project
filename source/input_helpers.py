from source.constants import ROLE_MSG
from source.role import Role


def get_input(prompt: str) -> str:
    return input(prompt).strip()


def get_role() -> Role:
    valid_roles = {role.value for role in Role}

    while True:
        match get_input(ROLE_MSG).lower():
            case Role.HOST.value:
                return Role.HOST
            case Role.CLIENT.value:
                return Role.CLIENT
            case _:
                print(f"Invalid role. Valid roles are: {valid_roles}")
