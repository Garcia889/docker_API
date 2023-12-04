from fastapi import FastAPI, Request
import joblib
from fastapi import UploadFile,File,HTTPException
from fastapi import APIRouter, Request
import os
from tempfile import NamedTemporaryFile
import pandas as pd
import csv
import codecs
from io import StringIO
import json
from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool
import os
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse

import os
import databases
import sqlalchemy
#link = f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["PGHOST"]}:5432/{os.environ["POSTGRES_DB"]}'
link = os.environ["DATABASE_URL"]#:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["PGHOST"]}:5432/{os.environ["POSTGRES_DB"]}'

database = databases.Database(link)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(link)
metadata.create_all(engine)



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
    return {"message": "Hello this a monitor tool for machine learning binary model "}

todos = []


@app.get("/clients")
async def get_clients(request: Request):

    lista_result=[]

    with engine.connect() as conn:
            result=conn.execute("""
                SELECT * 
                FROM clients
            """)
            for row in result:
                lista_result.append(list(row))
            #results = result.fetchall()

            

            df = pd.read_json(json.dumps(lista_result), orient='records')

            df.columns=['ID','SEX',
            'PAY_2',
            'PAY_4',
            'PAY_5',
            'PAY_6',
            'BILL_AMT1',
            'PAY_AMT2',
            'PAY_AMT4',
            'PAY_AMT5','TARGET_DEFAULT','TYPE_POP']
           
            df[['pred1','pred2']] = model.predict_proba(df)

          

            result=df.to_json(orient ='values')

            return result
    



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
    #df[['pred1','pred2']] = model.predict_proba(df)

    df.to_csv('data/test_pred.csv',index=True)

    return {"filename": file.filename}



@app.get("/download")
async def download_file(request: Request):
    df=pd.read_csv('data/test_pred.csv')

    df=df[['ID','SEX',
        'PAY_2',
        'PAY_4',
        'PAY_5',
        'PAY_6',
        'BILL_AMT1',
        'PAY_AMT2',
        'PAY_AMT4',
        'PAY_AMT5']]
   
   
    df[['pred1','pred2']] = model.predict_proba(df)
    result=df.to_json(orient ='values')
   
    #stream = io.StringIO()
    #df.to_csv(stream, index=False)
    #response = StreamingResponse(
    #    iter([stream.getvalue()]), media_type="text/csv")
    #response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return result






if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0', port=8000) # configurar host 
