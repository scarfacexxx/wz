-- Create database
CREATE DATABASE IF NOT EXISTS wizards_of_x;
USE wizards_of_x;

-- Players table
CREATE TABLE IF NOT EXISTS players (
    twitter_handle VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    house ENUM('Ravenclaw', 'Gryffindor', 'Slytherin', 'Hufflepuff'),
    level INT DEFAULT 1,
    xp INT DEFAULT 0,
    hp INT DEFAULT 100,
    bonus_galleons DECIMAL(10,2) DEFAULT 20.00,
    withdrawable_galleons DECIMAL(10,2) DEFAULT 0.00,
    spells JSON,
    potions JSON,
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    titles JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Active Duels table
CREATE TABLE IF NOT EXISTS active_duels (
    id INT PRIMARY KEY AUTO_INCREMENT,
    player1 VARCHAR(50),
    player2 VARCHAR(50),
    bet_amount DECIMAL(10,2),
    status VARCHAR(20),
    turn VARCHAR(50),
    hp1 INT,
    hp2 INT,
    combo_history JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player1) REFERENCES players(twitter_handle),
    FOREIGN KEY (player2) REFERENCES players(twitter_handle)
);

-- Banking tables
CREATE TABLE IF NOT EXISTS withdrawal_requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    twitter_handle VARCHAR(50),
    amount DECIMAL(10,2),
    fee DECIMAL(10,2),
    tx_hash VARCHAR(66),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    block_number BIGINT,
    FOREIGN KEY (twitter_handle) REFERENCES players(twitter_handle)
);

CREATE TABLE IF NOT EXISTS burn_queue (
    id INT PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL(10,2),
    scheduled_time TIMESTAMP,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS processed_transactions (
    tx_hash VARCHAR(66) PRIMARY KEY,
    block_number BIGINT,
    from_address VARCHAR(42),
    to_address VARCHAR(42),
    value DECIMAL(10,2),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20)
); 