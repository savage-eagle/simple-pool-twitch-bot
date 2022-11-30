CREATE TABLE IF NOT EXISTS pools (
    id integer PRIMARY KEY AUTOINCREMENT,
    author_id text NOT NULL,
    question text NOT NULL,
    created_at TIMESTAMP DEFAULT (datetime('now','localtime')),
    finished_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS poll_users (
    id integer PRIMARY KEY AUTOINCREMENT,
    voter_id INT,
    poll_id INT,
    vote TEXT, 
    created_at TIMESTAMP DEFAULT (datetime('now','localtime'))
);