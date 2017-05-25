import tornado.web
import tornado.ioloop
import os
import sqlite3
import random
import string

conn=sqlite3.connect("blog_db.sqlite")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        cur=conn.execute("SELECT title, id FROM article")
        self.render("templates/home.html",article_list = cur.fetchall())

class ArticleHandler(tornado.web.RequestHandler):
    def get(self,article_id):
        cur=conn.execute("SELECT * FROM article WHERE id='%s'"%(article_id))
        result=cur.fetchone()
        self.render("templates/article.html",title=result[1],article=result[2])

class AddArticle(tornado.web.RequestHandler):
    def get(self):
        if self.get_secure_cookie("lg") == None:
            self.write("please login first") 
        else:
            self.render("templates/add_article.html")

class AddResult(tornado.web.RequestHandler):
    def post(self):
        id=self.get_argument("id")
        title=self.get_argument("title")
        text=self.get_argument("text")
        conn.execute("INSERT INTO article VALUES('%s','%s','%s')"%(id,title,text))
        conn.commit()
        self.write('article added successfully!')

def generate_cookie(length):
    s=string.ascii_lowercase+string.digits+string.ascii_uppercase
    return ''.join(random.sample(s,length))

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/login.html")
    
    def post(self):
        user_name=self.get_argument("user_name")
        password=self.get_argument("password")
        cur=conn.execute("SELECT * FROM user WHERE user_name='%s' AND password='%s'"%(user_name,password))
        result=cur.fetchone()
        if(result==None):
            self.write("invalid user name or password")
        else:
            self.write("You are logged in!")
            self.set_secure_cookie("lg", generate_cookie(45))

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("lg")
        self.write("you are logged out!")

if __name__=="__main__":
    
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret":"__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    }

    app=tornado.web.Application([
        (r'/',MainHandler),
        (r'/login',LoginHandler),
        (r'/article/([_A-Za-z][_a-zA-Z0-9]*)',ArticleHandler),
        (r'/add_article',AddArticle),
        (r'/add_article/result',AddResult),
        (r'/logout',LogoutHandler),
    ],**settings)
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()