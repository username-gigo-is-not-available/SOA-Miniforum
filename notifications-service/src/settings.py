import os
from dotenv import load_dotenv

load_dotenv()

environment_variables_list = list(os.environ.keys())
environment_variables_dict = {
    env_var: os.getenv(env_var) for env_var in environment_variables_list
}

user_ids: list[int] = []

for variable_name, variable_value in environment_variables_dict.items():
    if not variable_value:
        raise RuntimeError(f"{variable_name} is not set!")


def set_connection_string(connection_string: str) -> str:
    for env_variable in environment_variables_list:
        if env_variable in connection_string:
            connection_string = connection_string.replace(env_variable, environment_variables_dict[env_variable])
    return connection_string
