import MySQLdb 
db=MySQLdb.connect("localhost","root","shreya","up")
mouse=db.cursor()
sql1="select * from mydatabase where country ='{}'".format("India")
mouse.execute(sql1)
data=mouse.fetchall()
db.commit()
print(len(data)," no of lines")
