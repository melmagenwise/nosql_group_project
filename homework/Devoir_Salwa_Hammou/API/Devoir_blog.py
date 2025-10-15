import fastapi
from fastapi.staticfiles import StaticFiles
import sqlmodel
import typing

app = fastapi.FastAPI()

class Article(sqlmodel.SQLModel, table=True): #on remplace l'agument "pydantic.BaseModel" par "sqlmodel.SQLModel, table=True" qui est un "enfant" de la classe pydantic.BaseModel
    id: int | None = sqlmodel.Field(primary_key=True) #cf cours base donnees pour cle primaire
    title: str
    content: str

#2 lignes suivantes: création d'une session de connexion à la base de données SQLite associée au fichier 'test.db'
engine = sqlmodel.create_engine("sqlite:///./test.db")
session = sqlmodel.Session(engine)

sqlmodel.SQLModel.metadata.create_all(engine) #creation/mise à jour des tables basée sur les modèles
app = fastapi.FastAPI()

#retourne la liste des articles (dans le backend) en mettant de "//" à la suite de l'adresse IP (dans barre de recherche)
@app.get("/articles") #j'ai mis de // car je n'arrivais pas à en ecrire qu'un seul sur le web 
def list_articles() -> typing.Sequence[Article]:
    query = sqlmodel.select(Article)
    return session.exec(query).all()

#creation lire un article
@app.get("/articles/{article_id}")
def read_article(article_id: int) -> Article:
    article = session.get(Article, article_id)  #article = session.get(Article, articles[article_id])
    if not article:
        raise fastapi.HTTPException(status_code=404, detail="Article not not found")
    return article
#pour creer un article
@app.post("/articles/") #@app.post("/articles/}")
def create_article(new_article:Article) -> Article: #ici new_article contient le body de la manière dont le new_article est construit dans le fichier html associé
    session.add(new_article)
    session.commit()
    session.refresh(new_article)
    return new_article
    #articles.append(new_article)
#pour faire un update
@app.put("/articles/{article_id}")
def update_article(article_id: int, updated_article: Article) -> Article:
    article = session.get(Article, article_id)
    if not article:
        raise fastapi.HTTPException(status_code=404, detail="Article not found")
    
    # Met à jour les champs avec les nouvelles données
    article.title = updated_article.title
    article.content = updated_article.content
    
    session.commit()
    session.refresh(article)
    return article

#pour supprimer un article
@app.delete("/articles/{article_id}")
def delete_article(article_id: int) -> Article:
    article = session.get(Article,article_id)
    if not article:
        raise fastapi.HTTPException(status_code=404, detail="Article not found")
    session.delete(article)
    session.commit()
    return article

app.mount("/", StaticFiles(directory="static", html=True), name="static") #lie aux pages contenues dans le fichier static


#pour consulter le backend: 
#pour consulter tout les articles : http://localhost:8000/articles
#pour consulter l'article 1: http://localhost:8000/articles/1 

#pour consulter le frontend:
#pour consulter la page admin : http://localhost:8000/admin.html
#pour consulter la page post : http://localhost:8000/post.html 
#pour consulter la page index : http://localhost:8000/index.html 