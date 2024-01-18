CREATE TABLE IF NOT EXISTS user_details (
    user_id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email_id TEXT UNIQUE,
    slack_member_id TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS baseband_info (
    site_id TEXT PRIMARY KEY,
    baseband_serial TEXT,
    baseband_type TEXT,
    cm_profile TEXT,
    site_manager TEXT,
    FOREIGN KEY (site_manager) REFERENCES user_details(user_id)
);

CREATE TABLE IF NOT EXISTS cm_policy (
    baseband_type TEXT,
    cm_profile TEXT,
    PRIMARY KEY (baseband_type, cm_profile)
);

CREATE TABLE IF NOT EXISTS events (
    event_timestamp TIMESTAMP,
    event_id TEXT PRIMARY KEY,
    event_detail TEXT
);

CREATE TABLE IF NOT EXISTS site_events (
    site_id TEXT,
    event_id TEXT,
    FOREIGN KEY (site_id) REFERENCES baseband_info(site_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    PRIMARY KEY (site_id, event_id)
);
