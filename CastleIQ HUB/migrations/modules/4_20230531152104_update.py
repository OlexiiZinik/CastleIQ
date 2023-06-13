from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "device" RENAME COLUMN "web_hook" TO "path";
        ALTER TABLE "deviceevent" ALTER COLUMN "event_schema" TYPE TEXT USING "event_schema"::TEXT;
        ALTER TABLE "deviceevent" ALTER COLUMN "event_schema" TYPE TEXT USING "event_schema"::TEXT;
        ALTER TABLE "deviceevent" ALTER COLUMN "event_schema" TYPE TEXT USING "event_schema"::TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "device" RENAME COLUMN "path" TO "web_hook";
        ALTER TABLE "deviceevent" ALTER COLUMN "event_schema" TYPE VARCHAR(500) USING "event_schema"::VARCHAR(500);
        ALTER TABLE "deviceevent" ALTER COLUMN "event_schema" TYPE VARCHAR(500) USING "event_schema"::VARCHAR(500);
        ALTER TABLE "deviceevent" ALTER COLUMN "event_schema" TYPE VARCHAR(500) USING "event_schema"::VARCHAR(500);"""
