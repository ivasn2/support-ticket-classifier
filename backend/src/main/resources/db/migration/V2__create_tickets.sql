CREATE TABLE tickets
(
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    description TEXT         NOT NULL,
    category_id BIGINT       NOT NULL REFERENCES categories (id),
    sentiment   VARCHAR(255),
    priority    INTEGER,
    created_at  TIMESTAMP,
    answered_at TIMESTAMP,
    status      VARCHAR(255)
);