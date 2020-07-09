import pyodbc 
computer="computer host"
computer=input("Enter Local Host for SQLExpress")
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server='+str(computer)+'\SQLEXPRESS;'
                      'Database=NYCGovJob_Test;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute('SELECT @@version')
for row in cursor:
    print(row)

# cursor.execute("CREATE TABLE Ftable(ID int, Descrip varchar(20))")
# cursor.commit()

# cursor.execute("INSERT INTO Ftable (ID, Descrip) VALUES (1,'Hello World' )")
# cursor.commit()
