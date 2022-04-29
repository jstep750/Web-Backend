from fastapi import FastAPI, HTTPException, status, Request
import sqlite3
import random

def get_words():
    lines = []
    with open('wordlist.txt') as f:
        lines = f.readlines()

    print("lines size: "+ str(len(lines)))
    word_list = lines[0].strip('"').split('","')
    print("word_list size: "+ str(len(word_list)))
    return word_list


def create_db():
    connect = sqlite3.connect("wordle.db")
    cursor = connect.cursor()
    cursor.execute("DROP TABLE IF EXISTS WORD_TABLE")
    cursor.execute("CREATE TABLE WORD_TABLE(word text)")
    word_list = get_words()

    for word in word_list:        
        #print(word)
        cursor.execute("INSERT INTO WORD_TABLE VALUES(?)", (word,))

    return cursor

app = FastAPI(root_path="/api/v1")
cursor = create_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


@app.get("/wordlist")
async def root():
    cursor.execute("SELECT * FROM WORD_TABLE")
    result = cursor.fetchall()
    words = str(list(res[0] for res in result)).strip('[]')
    #print(words)
    return {"words": words}

@app.get("/wordlist/addword/{word}", status_code=status.HTTP_201_CREATED)
async def read_item(word):
    cursor.execute("SELECT * FROM WORD_TABLE")
    result = cursor.fetchall()
    if (word,) in result: 
        raise HTTPException(status_code=404, detail="Word already exists!") 
    cursor.execute("INSERT INTO WORD_TABLE VALUES(?)", (word,))
    return {"word added": word}
    

@app.get("/wordlist/removeword/{word}")
async def read_item(word):
    cursor.execute("SELECT * FROM WORD_TABLE")
    result = cursor.fetchall()
    if (word,) in result: 
        cursor.execute("DELETE FROM WORD_TABLE WHERE word=?", (word,))
        return {"word removed": word}
    raise HTTPException(status_code=404, detail="Word not exist!") 
    

@app.get("/wordlist/checkvalid/{word}")
async def read_item(word):
    cursor.execute("SELECT * FROM WORD_TABLE")
    result = cursor.fetchall()
    if (word,) in result: 
        return {"word is valid": word} 
    raise HTTPException(status_code=404, detail="Word not valid!") 
    

@app.get("/guess/{word}")
async def read_item(word):
    cursor.execute("SELECT * FROM WORD_TABLE")
    result = cursor.fetchall()
    word_list = list(res[0] for res in result)
    answer = word_list[0]

    guess = word
    result = {}
    for a, g in zip(answer, guess):
        if(a == g) : result[g] = "green"
        elif(g in answer) : result[g] = "yellow"
        else : result[g] = "gray"
        print (a, g, result[g])
    return {"guess_result": result}

