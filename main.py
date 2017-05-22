import tornado.web
import tornado.ioloop
import sqlite3

conn=sqlite3.connect("blog_db.sqlite")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        cur=conn.execute("SELECT title, id FROM article")
        self.render("home.html",article_list = cur.fetchall())

class ArticleHandler(tornado.web.RequestHandler):
    def get(self,article_id):
        cur=conn.execute("SELECT * FROM article WHERE id='%s'"%(article_id))
        result=cur.fetchone()
        self.render("article.html",title=result[1],article=result[2])

class AddArticle(tornado.web.RequestHandler):
    def get(self):
        self.render("add_article.html")

class AddResult(tornado.web.RequestHandler):
    def post(self):
        id=self.get_argument("id")
        title=self.get_argument("title")
        text=self.get_argument("text")
        conn.execute("INSERT INTO article VALUES('%s','%s','%s')"%(id,title,text))
        conn.commit()
        self.write('article added successfully!')

if __name__=="__main__":
    
    app=tornado.web.Application([
        (r'/',MainHandler),
        (r'/article/([_A-Za-z][_a-zA-Z0-9]*)',ArticleHandler),
        (r'/add_article',AddArticle),
        (r'/add_article/result',AddResult),
    ])
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()