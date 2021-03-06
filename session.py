import psycopg2
from psycopg2 import Error
import config


class DateBase():
    """Обертка для работы с базой данных Екатерины"""
    def __init__(self) -> None:
        pass

    def session(self,param, request):
        """Принимает запрос (строкой)"""
        try:
            # Подключение к существующей базе данных
            self.connection = psycopg2.connect(user=config.USER,
                                        password=config.PASS,
                                        host=config.HOST,
                                        port=config.PORT,
                                        database=config.DATABASE)
            # Курсор для выполнения операций с базой данных
            self.sess = self.connection.cursor()

            #собсна выполнение запроса
            
            if param=="select":
                self.sess.execute(request)
                response = self.sess.fetchall()
                return response
            if param=="insert":
                self.sess.execute(request)
                self.connection.commit()
            

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            return error

        finally:
            if self.connection:
                self.sess.close()
                self.connection.close()
                print("Соединение с PostgreSQL закрыто")
    
    def open(self):
        # Подключение к существующей базе данных
        self.con = psycopg2.connect(user=config.USER,
                                        password=config.PASS,
                                        host=config.HOST,
                                        port=config.PORT,
                                        database=config.DATABASE)
        # Курсор для выполнения операций с базой данных
        cur= self.con.cursor()
        return cur

    def close(self):
        if self.con:
                self.connect.close()
                self.connection_.close()
                print("Соединение с PostgreSQL закрыто")



