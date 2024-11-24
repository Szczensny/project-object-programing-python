CREATE TABLE HABIT (
    UUID_ID varchar(46),
    CREATED_AT timestamp,
    NAME varchar(50),
    FREQUENCY ENUM('Daily', 'Weekly'),
    PRIMARY KEY(UUID_ID)
);
