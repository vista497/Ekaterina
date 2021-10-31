import psycopg2
from psycopg2 import Error

err=True

HOST="ec2-52-208-221-89.eu-west-1.compute.amazonaws.com"
DATABASE="da2u9nb473rkqt"
USER="hhaqhpjyhtobsz"
PASS="653c803a5d1a7f1cc86856eb1178c01b6ddbe6d16a31d8f760bad12f295444f5"
PORT="5432"


class DateBase():
    """Обертка для работы с базой данных Екатерины"""
    def __init__(self) -> None:
        pass

    def session(self,param, request):
        """Принимает запрос (строкой)"""
        try:
            # Подключение к существующей базе данных
            self.connection = psycopg2.connect(user=USER,
                                        password=PASS,
                                        host=HOST,
                                        port=PORT,
                                        database=DATABASE)
            # Курсор для выполнения операций с базой данных
            self.sess = self.connection.cursor()

            #собсна выполнение запроса
            
            if param=="select":
                self.sess.execute(request)
                response = self.sess.fetchone()
                return response
            if param=="insert":
                self.sess.execute(request)
                self.connection.commit()
            

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            return err

        finally:
            if self.connection:
                self.sess.close()
                self.connection.close()
                print("Соединение с PostgreSQL закрыто")
    
    def open(self):
        # Подключение к существующей базе данных
        self.connection_ = psycopg2.connect(user=USER,
                                        password=PASS,
                                        host=HOST,
                                        port=PORT,
                                        database=DATABASE)
        # Курсор для выполнения операций с базой данных
        self.connect = self.connection_.cursor()
        return self.connect

    def close(self):
        if self.connection_:
                self.connect.close()
                self.connection_.close()
                print("Соединение с PostgreSQL закрыто")



