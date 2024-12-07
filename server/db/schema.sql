BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "aggregators" (
	"id"	INTEGER NOT NULL,
	"guid"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "metric_values" (
	"metric_snapshot_id"	INTEGER NOT NULL,
	"metric_type_id"	INTEGER NOT NULL,
	"value"	NUMERIC NOT NULL,
	FOREIGN KEY("metric_snapshot_id") REFERENCES "metric_snapshots"("id"),
	FOREIGN KEY("metric_type_id") REFERENCES "metric_types"("id"),
	PRIMARY KEY("metric_snapshot_id","metric_type_id")
);
CREATE TABLE IF NOT EXISTS "metric_types" (
	"id"	INTEGER NOT NULL,
	"device_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	FOREIGN KEY("device_id") REFERENCES "devices"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "metric_snapshots" (
	"id"	INTEGER NOT NULL,
	"device_id"	INTEGER NOT NULL,
	"client_timestamp_utc"	INTEGER NOT NULL,
	"client_timezone_mins"	INTEGER NOT NULL,
	"server_timestamp_utc"	INTEGER NOT NULL,
	"server_timezone_mins"	INTEGER NOT NULL,
	FOREIGN KEY("device_id") REFERENCES "devices"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "devices" (
	"id"	INTEGER NOT NULL,
	"aggregator_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"ordinal"	INTEGER NOT NULL,
	FOREIGN KEY("aggregator_id") REFERENCES "aggregators"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
