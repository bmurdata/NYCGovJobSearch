import pyodbc 
computer="localhost"

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server='+str(computer)+'\SQLEXPRESS;'
                      'Database=NYCGovJob_Test;'
                      'Trusted_Connection=yes;'
                      'autocommit=True;')

cursor = conn.cursor()
cursor.execute('SELECT @@version')
for row in cursor:
    print(row)

cursor.execute('SELECT * FROM Ftable')
for row in cursor:
    print(row)
#cursor.execute("INSERT INTO Ftable (ID,Descrip) VALUES (5,'Zamirah')")
#cursor.commit()
linkBase="https://a127-jobs.nyc.gov/psc/nycjobs/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId={jobId}&PostingSeq=1&"
#CREATE PROCEDURE newSchema.PutNewLinkIntoDB
#@newLink NVARCHAR(2083), @catName NVARCHAR(250), @longcat NVARCHAR(250),@jobid INT
def toDB_test(newlink, catName,longcat,jobid):
    #sqlexec="CALL newSchema.PutNewLinkIntoDB ('{nlink}', '{cName}', '{lCat}', {jId})".format(nlink=newlink,cName=catName,lCat=longcat,jId=jobid)
    #sqlexec="CALL newSchema.test3 ('{link}')".format(link=catName)
    sqlexec="{CALL newSchema.PutNewLinkIntoDB (?,?,?,?)}"
    params=(newlink,catName,longcat,jobid)
    print("Executing "+sqlexec)
    #cursor.execute("{"+ sqlexec+"}")
    cursor.execute(sqlexec,params)
    cursor.commit()

def toDB(newlink, catName,longcat,jobid):
    #sqlexec="CALL newSchema.PutNewLinkIntoDB ('{nlink}', '{cName}', '{lCat}', {jId})".format(nlink=newlink,cName=catName,lCat=longcat,jId=jobid)
    #sqlexec="CALL newSchema.test3 ('{link}')".format(link=catName)
    sqlexec="{CALL newSchema.PutNewLinkIntoDB (?,?,?,?)}"
    params=(newlink,catName,longcat,jobid)
    print("Executing "+sqlexec)
    #cursor.execute("{"+ sqlexec+"}")
    cursor.execute(sqlexec,params)
    cursor.commit()
    try:
        for row in cursor:
            print(row)
    except:
        print("Row didnt print. Womp")