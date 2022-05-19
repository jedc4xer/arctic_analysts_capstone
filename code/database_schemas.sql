/* SCHEMA CREATION */

USE arctic_analysts_capstone;

CREATE TABLE year (
    YearID INT PRIMARY KEY IDENTITY(1,1),
    Year INT NOT NULL,
    CONSTRAINT uq_year
        UNIQUE (Year)
);

CREATE TABLE month (
    MonthID INT PRIMARY KEY,
    Month VARCHAR(3) NOT NULL,
    CONSTRAINT uq_Month
        UNIQUE (Month)
);

CREATE TABLE county (
    FIPS VARCHAR(7) NOT NULL,
    County VARCHAR(100) NOT NULL,
    CONSTRAINT pk_county
        PRIMARY KEY (FIPS),
    CONSTRAINT uq_county
        UNIQUE (County)
);

CREATE TABLE median_income (
    FIPS VARCHAR(7) NOT NULL,
    YearID INT NOT NULL,
    AgeGroup VARCHAR(20) NOT NULL,
    MedianIncome INT NOT NULL,
    CONSTRAINT fk_median_income_FIPS
        FOREIGN KEY (FIPS)
        REFERENCES county(FIPS),
    CONSTRAINT fk_median_income_year
        FOREIGN KEY (YearID)
        REFERENCES year(YearID),
    CONSTRAINT pk_median_income
        PRIMARY KEY (FIPS,YearID,AgeGroup)
);

CREATE TABLE main_table (
    FIPS VARCHAR(7) NOT NULL,
    YearID INT NOT NULL,
    MonthID INT NOT NULL,
    NewUnits INT NOT NULL,
    NewBuildings INT NOT NULL,
    MedianHousePrice INT NULL,
    AverageRate NUMERIC(5,2) NOT NULL,
    AveragePoints NUMERIC(4,2) NOT NULL,
    CONSTRAINT fk_main_table_FIPS
        FOREIGN KEY (FIPS)
        REFERENCES county(FIPS),
    CONSTRAINT fk_main_table_year
        FOREIGN KEY (YearID)
        REFERENCES year(YearID),
    CONSTRAINT fk_main_table_month
        FOREIGN KEY (MonthID)
        REFERENCES month(MonthID),
    CONSTRAINT pk_main_table 
        PRIMARY KEY (FIPS, YearID, MonthID)
);