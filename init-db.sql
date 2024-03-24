-- Erstellung der Tabelle User
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL,
    email VARCHAR(128) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    token VARCHAR(32),
    token_expiration TIMESTAMP
);

-- Erstellung der Tabelle workplacedesk
CREATE TABLE workplacedesk (
    id SERIAL PRIMARY KEY,
    price FLOAT NOT NULL,
    info VARCHAR(256)
);

-- Erstellung der Tabelle Reservation
CREATE TABLE reservation (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    workplace_desk_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (workplace_desk_id) REFERENCES workplacedesk(id),
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);