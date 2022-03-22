from pydantic import BaseSettings


class Environment(BaseSettings):
    db_hostname: str
    db_port: str
    db_username: str
    db_session: str
    db_name: str


env_vars = Environment()
