SELECT * FROM spacex.spacextable;
SELECT DISTINCT Launch_Site FROM spacex;
select sum(PAYLOAD_MASS__KG_) from spacextable
where Customer='NASA (CRS)';
select avg(PAYLOAD_MASS__KG_) FROM SPACEXTABLE
WHERE Booster_Version like 'F9 v1.1%';
SELECT MIN(Date) AS First_Successful_Landing_Date
FROM spacextable
WHERE Landing_Outcome = 'Success (ground pad)';
SELECT Booster_Version
FROM spacextable
WHERE Landing_Outcome = 'Success (drone ship)'
  AND Payload_Mass__KG_ > 4000
  AND Payload_Mass__KG_ < 6000;
SELECT 
    CASE
        WHEN Mission_Outcome LIKE 'Success%' THEN 'Success'
        WHEN Mission_Outcome LIKE 'Failure%' THEN 'Failure'
        ELSE 'Other'
    END AS Outcome_Category,
    COUNT(*) AS Total_Count
FROM spacextable
GROUP BY Outcome_Category;
SELECT Booster_Version
FROM spacextable
WHERE Payload_Mass__KG_ = (
    SELECT MAX(Payload_Mass__KG_)
    FROM spacextable
);
SELECT 
    CASE 
        WHEN SUBSTR(Date, 6, 2) = '01' THEN 'January'
        WHEN SUBSTR(Date, 6, 2) = '02' THEN 'February'
        WHEN SUBSTR(Date, 6, 2) = '03' THEN 'March'
        WHEN SUBSTR(Date, 6, 2) = '04' THEN 'April'
        WHEN SUBSTR(Date, 6, 2) = '05' THEN 'May'
        WHEN SUBSTR(Date, 6, 2) = '06' THEN 'June'
        WHEN SUBSTR(Date, 6, 2) = '07' THEN 'July'
        WHEN SUBSTR(Date, 6, 2) = '08' THEN 'August'
        WHEN SUBSTR(Date, 6, 2) = '09' THEN 'September'
        WHEN SUBSTR(Date, 6, 2) = '10' THEN 'October'
        WHEN SUBSTR(Date, 6, 2) = '11' THEN 'November'
        WHEN SUBSTR(Date, 6, 2) = '12' THEN 'December'
    END AS Month_,
    Landing_Outcome,
    Booster_Version,
    Launch_Site
FROM spacextable
WHERE Landing_Outcome = 'Failure (drone ship)'
  AND SUBSTR(Date, 1, 4) = '2015';
SELECT Landing_Outcome, COUNT(*) AS Outcome_Count
FROM spacextable
WHERE Date BETWEEN '2010-06-04' AND '2017-03-20'
GROUP BY Landing_Outcome
ORDER BY Outcome_Count DESC;