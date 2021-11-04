import session

SELECT="select"
INSERT="insert"

class Repository():
    def __init__(self):
        self.db=session.DateBase()

    def urlFromName(self, value):
        """Возвращает URL, принимает имя URL"""
        query="select url from web where name="+value
        resp=self.webStr=self.db.session(SELECT, query)
        return resp

    def insertUrl(self, name, url):
        """Добавляет новый URL c его именем"""
        query="insert into web (name, url) values ('"+name+ "', '"+url+"')"
        self.webStr=self.db.session(INSERT, query)
    
    def tgReg(self, firstName, lastName, age, tg_id, status):
        """Добавляет нового пользователя из чат бота"""

        query="insert into ekaterina.people_tg (first_name, last_name, age, tg_id, status) values ('"+firstName+"', '"+lastName+"','"+str(age)+"','"+str(tg_id)+"','"+status+"')"
        resp=self.db.session(INSERT, query)

    def getPersonById(self, tg_id_):
        """Возвращает имя фамилию возраст и айди""" 

        query="select first_name,last_name, age, tg_id, status from ekaterina.people_tg where tg_id="+str(tg_id_)
        response =self.db.session(SELECT, query)
        if len(response)!=0:
            for row in response:
                first_name=row[0]
                last_name=row[1]
                age=row[2]
                tg_id=row[3]
                status=row[4]
        else: 
            first_name, last_name, age, tg_id, status = "none", "none", 0, "none", "none"
        return first_name, last_name, age, tg_id, status


        
    
 
