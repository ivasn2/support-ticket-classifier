CREATE TABLE prioritization_results
(
    id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ticket_id  BIGINT NOT NULL REFERENCES tickets (id) UNIQUE,
    sentiment  VARCHAR(255),
    priority   INTEGER,
    confidence DOUBLE PRECISION
);