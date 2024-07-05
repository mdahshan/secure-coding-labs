-- Create the users table
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- Create the accounts table
CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    balance REAL NOT NULL DEFAULT 0.0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Insert data into the users table
INSERT INTO users (username, password) VALUES ('alice', 'alice_pass');
INSERT INTO users (username, password) VALUES ('bob', 'bob_pass');
INSERT INTO users (username, password) VALUES ('mostafa', 'mostafa_pass');

-- Insert data into the accounts table
-- Assuming Alice's user_id is 1, Bob's user_id is 2, and Mostafa's user_id is 3
INSERT INTO accounts (user_id, balance) VALUES (1, 1000.00);  -- Alice's balance
INSERT INTO accounts (user_id, balance) VALUES (2, 1500.50);  -- Bob's balance
INSERT INTO accounts (user_id, balance) VALUES (3, 2000.75);  -- Mostafa's balance;
