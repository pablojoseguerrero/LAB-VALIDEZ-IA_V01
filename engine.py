"""Validated statistical routines for qualitative interview content validity."""
from collections import Counter
from math import sqrt
from scipy.stats import binomtest

def aiken(values,low=1,high=5):
    vals=[int(v) for v in values]
    if not vals or low>=high or any(v<low or v>high for v in vals): raise ValueError('Valores fuera de la escala')
    return round(sum(v-low for v in vals)/(len(vals)*(high-low)),4)

def lawshe(values):
    if not values: raise ValueError('Sin evaluaciones')
    return round((2*sum(str(v).strip().lower() in ('esencial','1','sí','si','true') for v in values)/len(values))-1,4)

def binomial(values,p0=0.5,alternative='greater'):
    if not 0<p0<1: raise ValueError('p0 debe estar entre 0 y 1')
    n=len(values); k=sum(str(x).lower().strip() in ('sí','si','1','true','aprobado') for x in values)
    if not n: raise ValueError('Sin evaluaciones')
    return {'favorables':k,'total':n,'proporcion':round(k/n,4),'p_value':round(float(binomtest(k,n,p=p0,alternative=alternative).pvalue),6),'hipotesis_nula':p0,'alternativa':alternative}

def kappa(a,b):
    if len(a)!=len(b) or not a: raise ValueError('Los jueces deben evaluar las mismas unidades')
    a=[str(x).strip().lower() for x in a];b=[str(x).strip().lower() for x in b]
    n=len(a); po=sum(x==y for x,y in zip(a,b))/n
    ca=Counter(a);cb=Counter(b)
    pe=sum(ca[k]*cb[k] for k in set(ca)|set(cb))/(n*n)
    return {'kappa':round((po-pe)/(1-pe),4) if pe<1 else (1.0 if po==1 else None),'acuerdo_observado':round(po,4),'acuerdo_azar':round(pe,4),'unidades':n}

def analyze(rows,method='aiken',low=1,high=5,p0=.5):
    """Long format: item, criterion, expert, value. Distinct expert per item/criterion."""
    if not rows: raise ValueError('La base de datos está vacía')
    groups={}
    for r in rows:
        item=str(r.get('item','')).strip(); crit=str(r.get('criterion','')).strip();expert=str(r.get('expert','')).strip(); value=str(r.get('value','')).strip()
        if not all((item,crit,expert,value)): raise ValueError('Cada fila necesita item, criterion, expert y value')
        key=(item,crit)
        if key not in groups:groups[key]={}
        if expert in groups[key]: raise ValueError(f'Valoración duplicada: {item}, {crit}, {expert}')
        groups[key][expert]=value
    out=[]
    for (item,crit), judgments in sorted(groups.items()):
        values=list(judgments.values())
        if method=='aiken': result={'v_aiken':aiken(values,low,high)}
        elif method=='lawshe': result={'cvr':lawshe(values)}
        elif method=='binomial':result=binomial(values,p0)
        else:raise ValueError('Método de análisis no disponible')
        out.append({'item':item,'criterion':crit,'n_experts':len(values),**result})
    return {'method':method,'results':out,'total_rows':len(rows),'warning':'Resultados de validez de contenido: no equivalen por sí solos a validez global del instrumento.'}