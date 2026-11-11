from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from io import BytesIO
import csv, re, json, zipfile
from pypdf import PdfReader
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from engine import analyze, aiken, lawshe, binomial, kappa

ROOT=Path(__file__).resolve().parent
app=FastAPI(title='LAB-VALIDEZ IA',version='1.0.0')
app.mount('/static',StaticFiles(directory=ROOT/'static'),name='static')
@app.get('/')
def index():return FileResponse(ROOT/'static/index.html')
@app.get('/health')
def health():return {'status':'ok','version':'1.0.0'}

async def extract(f:UploadFile):
    data=await f.read()
    if len(data)>12*1024*1024:raise HTTPException(413,'Archivo superior a 12 MB')
    name=(f.filename or '').lower()
    try:
        if name.endswith('.pdf'):return '\n'.join((p.extract_text() or '') for p in PdfReader(BytesIO(data)).pages)
        if name.endswith('.docx'):return '\n'.join(p.text for p in Document(BytesIO(data)).paragraphs)+'\n'+'\n'.join(' | '.join(c.text for c in r.cells) for t in Document(BytesIO(data)).tables for r in t.rows)
        if name.endswith(('.txt','.csv')):return data.decode('utf-8-sig')
        if name.endswith('.xlsx'):
            # For extraction only; spreadsheets are not modified here.
            from artifact_tool import Blob, SpreadsheetFile
            # XLSX files should be supplied as CSV for structured parsing; report this explicitly.
            raise ValueError('Para cuadros XLSX, exporte a CSV UTF-8 desde Excel y vuelva a cargarlo.')
        raise ValueError('Formatos admitidos: PDF, DOCX, TXT y CSV')
    except Exception as e:raise HTTPException(422,str(e))

def detect_items(text):
    # Recover questions split over PDF text lines, stopping at next interview item.
    pattern=re.compile(r'\b(E\s*[-–]\s*\d+)\b',re.I)
    matches=list(pattern.finditer(text)); items=[]
    for i,m in enumerate(matches):
        code=re.sub(r'\s+','',m.group(1)).upper().replace('–','-')
        segment=text[m.end():(matches[i+1].start() if i+1<len(matches) else len(text))]
        q=re.search(r'¿[\s\S]{10,900}?\?',segment)
        if q and not any(x['id']==code for x in items):
            question=re.sub(r'\s+',' ',q.group(0)).strip()
            items.append({'id':code,'question':question,'indicator':'Por confirmar'})
    return items

@app.post('/api/parse')
async def parse(instrument:UploadFile=File(...),categorization:UploadFile=File(...)):
    a=await extract(instrument); b=await extract(categorization)
    return {'instrument_text':a[:45000],'categorization_text':b[:45000],'items':detect_items(a),'recommendation':'Juicio de expertos + V de Aiken' if ('¿' in a or 'entrevista' in a.lower()) else 'Requiere revisión del tipo de instrumento','notes':['Confirmar manualmente los ítems y su relación con los indicadores antes de generar la ficha.','KMO/Bartlett no corresponden a preguntas abiertas sin matriz cuantitativa adecuada.']}

class AnalyzeRequest(BaseModel):
    method:str='aiken'; rows:list[dict]; low:int=1;high:int=5;p0:float=.5
@app.post('/api/analyze')
def analyze_api(r:AnalyzeRequest):
    try:return analyze(r.rows,r.method,r.low,r.high,r.p0)
    except ValueError as e:raise HTTPException(422,str(e))

class KappaRequest(BaseModel):
    judge1:list;judge2:list
@app.post('/api/kappa')
def kappa_api(r:KappaRequest):
    try:return kappa(r.judge1,r.judge2)
    except ValueError as e:raise HTTPException(422,str(e))

class ExportRequest(BaseModel):
    title:str='Informe de validez de contenido';author:str='Prof. Dr. Pablo José Guerrero, PhD.';items:list[dict]=[];results:list[dict]=[];method:str='aiken';notes:str=''

def report_lines(r):
    lines=[r.title,'RED CTII.AI | LAB-VALIDEZ IA','Autor de la plataforma: Prof. Dr. Pablo José Guerrero, PhD.','Método: '+r.method,'','1. INSTRUMENTO EVALUADO']
    for x in r.items:lines.append(f"{x.get('id','')}: {x.get('question','')} | Indicador: {x.get('indicator','')}")
    lines+=['','2. RESULTADOS DE LA EVALUACIÓN']
    if not r.results:lines.append('Pendiente: no se han proporcionado valoraciones de expertos.')
    else:
        for z in r.results: lines.append(' | '.join(f'{k}: {v}' for k,v in z.items()))
    lines+=['','3. INTERPRETACIÓN Y LIMITACIONES',r.notes or 'Interpretar cada coeficiente según número de jueces, escala y criterios preestablecidos. Los resultados no implican validez global automática.','', 'Referencia: Sánchez Espejo, F. G. (2020). Estadística para tesis y uso del SPSS. Centrum Legalis.','© 2026 Prof. Dr. Pablo José Guerrero, PhD. | RED CTII.AI']
    return lines

@app.post('/api/export/docx')
def export_docx(r:ExportRequest):
    d=Document();d.add_heading(r.title,0)
    for line in report_lines(r)[1:]:
        if re.match(r'^\d\. ',line):d.add_heading(line,level=2)
        else:d.add_paragraph(line)
    b=BytesIO();d.save(b);b.seek(0)
    return StreamingResponse(b,media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',headers={'Content-Disposition':'attachment; filename="informe_validez.docx"'})
@app.post('/api/export/pdf')
def export_pdf(r:ExportRequest):
    b=BytesIO();c=canvas.Canvas(b,pagesize=A4); width,height=A4;y=height-52
    for line in report_lines(r):
        if re.match(r'^\d\. ',line):c.setFont('Helvetica-Bold',12)
        else:c.setFont('Helvetica',9)
        for part in simpleSplit(line,'Helvetica',9,width-88) or ['']:
            if y<60:c.showPage();y=height-52
            c.drawString(44,y,part);y-=15
        y-=5
    c.save();b.seek(0)
    return StreamingResponse(b,media_type='application/pdf',headers={'Content-Disposition':'attachment; filename="informe_validez.pdf"'})