from fastapi import FastAPI
from models import Todo
import joblib
from fastapi import UploadFile,File,HTTPException
import os
from tempfile import NamedTemporaryFile
import pandas as pd
import csv
import codecs
from io import StringIO
app = FastAPI()


obj = open("estimator_hyper_xgb.joblib","rb")
model=joblib.load(obj)


datadir="data/"

import os
dir="data"
## If folder doesn't exists, create it ##
if not os.path.isdir(dir):
    os.mkdir(dir)

        


@app.get("/")
async def root():
    return {"message": "Hello World"}

todos = []

# Get all todos
@app.get("/todos")
async def get_todos():
    return {"todos": todos}

# Get single todo
@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return{"todo": todo}
    return {"message": "No todos found"}

# Create a todo
@app.post("/todos")
async def create_todos(todo: Todo):
    todos.append(todo)
    return {"message": "Todo has been added"}
 
# Update a todo
@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo_obj: Todo):
    for todo in todos:
        if todo.id == todo_id:
            todo.id = todo_id
            todo.item = todo_obj.item
            return {"todo": todo}
    return {"message":"No todos found to update"}


# Delete a todo
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return{"message": "todo has been DELETED!"}
    return {"message": "No todos found"}



@app.post("/check")
def upload_file(file: UploadFile = File(...)):
    temp = NamedTemporaryFile(delete=False)
    try:
        try:
            contents = file.file.read()
            with temp as f:
                f.write(contents);
            #with open(f{datadir}{file.filename}) as f:
            #    f.write(contents);
        except Exception:
            raise HTTPException(status_code=500, detail='Error on uploading the file')
        finally:
            file.file.close()
            
        # Upload the file to your S3 service using `temp.name`
        #s3_client.upload_file(temp.name, 'local', 'myfile.txt')
        
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        #temp.close()  # the `with` statement above takes care of closing the file
        os.remove(temp.name)  # Delete temp file
    
    print(contents)  # Handle file contents as desired
    s=str(contents,'utf-8')
    data=StringIO(s)
    df=pd.read_csv(data)
    data.close()
    #contents_df=pd.DataFrame(contents)
    df[['pred1','pred2']] = model.predict_proba(df)

    df.to_csv('data/test_pred.csv',index=True)

    return {"filename": file.filename}

#app.run_server(debug=True, port=8001)