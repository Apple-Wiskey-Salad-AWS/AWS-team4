from fastapi import FastAPI
from fastapi.responses import JSONResponse

import pandas as pd
import ast
from endpoint_util import EndpointUtil


local_folder_path = '/aaa/test/'
endpoint_name = "ep-xray-detection-4"
bucket_name = "newdataa"
endpoint = EndpointUtil(bucket_name, endpoint_name, local_folder_path)


app = FastAPI()

@app.get("/")
async def hello():
    return {"hello": "world"}


@app.get("/{user_id}/{threshold}")
async def root(user_id: str, threshold: str):
    pred_df = endpoint.call(int(user_id), float(threshold))
    print(f'pred_df = {type(pred_df)}')
    
    # Convert the recommendations to a JSON-serializable format
    pred_df = pred_df.to_dict(orient='records')

    return JSONResponse(content=pred_df)


@app.get('/get_class_info')
async def get_class_info():
    # Read the classes.txt file
    with open('classes.txt', 'r') as file:
        # Read the contents of the file
        data = file.read()
    
    # Extract the class_names dictionary using AST
    class_dict = ast.literal_eval(data.split('class_names = ')[1])
    
    return JSONResponse(content=class_dict)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("server:app", host='0.0.0.0', port=8080, workers=1)
