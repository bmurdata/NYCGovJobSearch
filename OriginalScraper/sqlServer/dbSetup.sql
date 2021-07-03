
USE NYCGovJob_Test
GO
--Make the schema
CREATE SCHEMA newSchema
--Make the table to be used to store data
CREATE TABLE newSchema.jobDataproto(
jobData_id INT  IDENTITY PRIMARY KEY,
jobid INT NOT NULL,
long_agency NVARCHAR(500),
agency_acronym NVARCHAR(10),
posted DATE,
job_title NVARCHAR(250),
job_loc NVARCHAR(100),
joblink NVARCHAR(2083),
);

GO
--Make a stored procedure in the new schema
CREATE PROCEDURE newSchema.PutNewLinkIntoDB
( @newLink NVARCHAR(2083), @catName NVARCHAR(250), @longcat NVARCHAR(250),@jobid INT)
AS
BEGIN
--Insert into the table if the jobid is unique for the acronym(POA, HLT, etc..)
IF NOT EXISTS (SELECT * FROM jobDataproto WHERE jobid = @jobid AND agency_acronym=@catName)
BEGIN
INSERT INTO jobDataproto (joblink,jobid,long_agency,agency_acronym) VALUES 
(@newLink,@jobid,@longcat,@catName)
SELECT 'Inserted new values in database'
END
ELSE
BEGIN
SELECT 'Already in Database'
END
END
--Test of the stored procedure
--EXEC newSchema.PutNewLinkIntoDB "1212", "121212","dadasdadadwa",2
--SELECT * FROM newSchema.jobDataproto
