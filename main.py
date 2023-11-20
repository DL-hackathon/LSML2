import torch
import time
import datetime
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi import Form
from transformers import AutoTokenizer, BertForSequenceClassification

'''
Main file to start FastAPI
'''


app = FastAPI()
app.mount("/static", StaticFiles(directory='static'), name="static")
templates = Jinja2Templates(directory='templates')

base_model = "static/model_2ep/"
tokenizer = AutoTokenizer.from_pretrained(base_model)
model = BertForSequenceClassification.from_pretrained(base_model)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("main_page.html",
                                      {"request": request})


@app.get('/inference')
async def inference(request: Request):
    return templates.TemplateResponse("inference.html",
                                      {"request": request})



def format_time(elapsed):
    '''
    Takes a time in seconds and returns a string hh:mm:ss
    '''
    # Round to the nearest second.
    elapsed_rounded = int(round((elapsed)))

    # Format as hh:mm:ss
    return str(datetime.timedelta(seconds=elapsed_rounded))

@app.post("/show_result")
async def show_result(request: Request,
                    text: str = Form(...)):
    if not text or len(text) < 10:
        message = 'Input field should contain at least 10 symbols! Please go back and try again.'
        return templates.TemplateResponse("no_inference.html",
                                          {"request": request,
                                           "message": message})
    
    since = time.time()
    text_tokenized = tokenizer(text, truncation=True,
                               max_length=512, return_tensors='pt')
    model.eval()
    with torch.no_grad():
        out = model(**text_tokenized)
    result = out.logits.argmax().item()
    if result:
        answer = "Hate! Most likely your text has curse words!"
    else:
        answer = 'Non-hate!'
    
    time_elapsed = format_time(time.time() - since)

    return templates.TemplateResponse("show_result.html",
                                      {"request": request,
                                       "text": text,
                                       "answer": answer,
                                       "time_elapsed": time_elapsed})

@app.get("/download/ipynb")
def download_ipynb():
    return FileResponse(path='static/fp.ipynb', filename='model_code_(Lazarev).ipynb')

@app.get("/download/pdf")
def download_pdf():
    return FileResponse(path='static/fp.pdf', filename='model_code_(Lazarev).pdf')

@app.get("/download/script")
def download_pdf():
    return FileResponse(path='main.py', filename='web_service_script_(Lazarev).py')