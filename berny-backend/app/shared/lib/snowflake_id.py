from snowflake import SnowflakeGenerator
from app.shared.config import settings

snowflake_gen = SnowflakeGenerator(instance=settings.WORKER_ID)

def get_snowflake_id() -> int:
    return next(snowflake_gen) #type: ignore