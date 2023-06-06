from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "device" ADD "protocol" VARCHAR(10) NOT NULL  DEFAULT 'http';
        CREATE TABLE IF NOT EXISTS "deviceevent" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "description" VARCHAR(500) NOT NULL,
    "event_schema" VARCHAR(500) NOT NULL,
    "device_id" INT NOT NULL REFERENCES "device" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "device" DROP COLUMN "protocol";
        DROP TABLE IF EXISTS "deviceevent";"""
