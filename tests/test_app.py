from fastapi.testclient import TestClient
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import app
from engine import aiken,lawshe,binomial,kappa,analyze
C=TestClient(app)
def test_math():
 assert aiken([5,5,4,5,4])==.9
 assert lawshe(['esencial']*9+['útil'])==.8
 assert binomial(['sí']*9+['no'])['p_value']==.010742
 assert kappa(['si','si','si','no','no','si','no','no'],['si','si','no','no','no','si','si','no'])['kappa']==.5

def test_navigation():
 assert C.get('/').status_code==200
 assert b'LAB-VALIDEZ' in C.get('/').content
 assert C.get('/static/logo.png').status_code==200
 assert C.get('/health').json()['status']=='ok'

def test_evaluate_and_exports():
 rows=[{'item':'E-1','criterion':'Pertinencia','expert':f'J-{i}','value':str(v)} for i,v in enumerate([5,5,4,5,4],1)]
 j=C.post('/api/analyze',json={'method':'aiken','rows':rows});assert j.status_code==200
 assert j.json()['results'][0]['v_aiken']==.9
 assert C.post('/api/analyze',json={'method':'aiken','rows':rows+rows}).status_code==422
 for fmt,ctype in [('docx','wordprocessingml'),('pdf','application/pdf')]:
  r=C.post('/api/export/'+fmt,json={'items':[{'id':'E-1','question':'Pregunta de prueba','indicator':'Plan'}],'results':j.json()['results']})
  assert r.status_code==200 and ctype in r.headers['content-type'] and len(r.content)>500

def test_document_parser():
 p=Path(__file__).resolve().parents[1]/'samples/entrevista_ejemplo.pdf'
 r=C.post('/api/parse',files={'instrument':('entrevista.pdf',p.read_bytes(),'application/pdf'),'categorization':('categorias.txt',b'Indicadores: Plan instruccional','text/plain')})
 assert r.status_code==200, r.text
 assert 'E-1' in r.text and r.json()['items']