from fastapi import FastAPI, HTTPException, status
import sqlite3
from datetime import datetime

date = datetime.today().strftime('%Y-%m-%d')

def answer_db():
    connect = sqlite3.connect("answer.db")
    cursor = connect.cursor()
    cursor.execute("DROP TABLE IF EXISTS ANSWER_TABLE")
    cursor.execute("CREATE TABLE ANSWER_TABLE(answer text, date text)")
    cursor.execute("INSERT INTO ANSWER_TABLE VALUES(?,?)", ("cigar",date,))
    return cursor

app = FastAPI()
connect = sqlite3.connect("wordle.db")
cursor = connect.cursor()
cursor2 = answer_db()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/answer/add/{word}", status_code=status.HTTP_201_CREATED)
async def read_item(word):
    cursor2.execute("SELECT * FROM ANSWER_TABLE WHERE date=?", (date,))
    result = list(map(lambda x : x[0], cursor2.fetchall()))
    print(result)
    if word in result: 
        raise HTTPException(status_code=404, detail="Word already exists!") 
    cursor2.execute("INSERT INTO ANSWER_TABLE VALUES(?,?)", (word, date,))
    return {"answer added": word}

@app.get("/answer/remove/{word}", status_code=status.HTTP_201_CREATED)
async def read_item(word):
    cursor2.execute("SELECT * FROM ANSWER_TABLE WHERE date=?", (date,))
    result = list(map(lambda x : x[0], cursor2.fetchall()))
    print(result)
    if word in result: 
        cursor2.execute("DELETE FROM ANSWER_TABLE WHERE answer=? AND date=?", (word, date,))
        return {"answer removed": word}
    raise HTTPException(status_code=404, detail="Word not exists!") 


@app.get("/guess/{word}")
async def read_item(word):
    cursor.execute("SELECT * FROM WORD_TABLE")
    result = cursor.fetchall()
    cursor2.execute("SELECT * FROM ANSWER_TABLE WHERE date=?", (date,))
    fetch = cursor2.fetchone()

    if not fetch: 
        raise HTTPException(status_code=500, detail="No Answer!") 

    answer = fetch[0]
    guess = word
    result = {}
    for a, g in zip(answer, guess):
        if(a == g) : result[g] = "green"
        elif(g in answer) : result[g] = "yellow"
        else : result[g] = "gray"
        print (a, g, result[g])
    return {"guess_result": result}

