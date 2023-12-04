create table clients( 
    ID int,
    SEX int,
    PAY_2 float,
    PAY_4 float,
    PAY_5 float,
    PAY_6 float,
    BILL_AMT1 float,
    PAY_AMT2 float,
    PAY_AMT4 float,
    PAY_AMT5 float,
    TARGET_DEFAULT int,
    TYPE_POP varchar(80)
);
COPY clients
FROM '/BD/data/test.csv'
DELIMITER ','
CSV HEADER
NULL as 'NA';

