from typing import List,NamedTuple
import logging

MARKER="---"
SEPA=" | "
BETWEEN=1

STMT="STMT_TEXT"
BPNAME="BP_NAME"
STMTCUT=40

class MONELEM(NamedTuple) :
    
    labels : List[str]
    vals : List[List[str]]
    

def transfortolist(l : str, labels: List[str]) -> List[str] :
    a : List[str] = l.split(' ')
    # remove empty
    res : List[str] = [ l.strip() for l in a if len(l.strip()) != 0]
    if STMT in labels :
        i : int  = labels.index(STMT)
        begst: str = res[i]
        b : str = l.find(begst)
        res = res[0:i]
        sta = l[b:b+STMTCUT]
        res.append(sta)
        
    if BPNAME in labels and len(res) == len(labels) + 1:
        i : int = labels.index(BPNAME)
        res[i] = res[i] + res[i+1]
        res = res[0:i+1] + res[i+2:]
                
    return res

# ---------------------
# lines
# ---------------------

def writebetween(f) :
    for _ in range(BETWEEN) :
        f.write(SEPA)
        
def writeempty(f,e : MONELEM) :
    for _ in range(len(e.vals)) :
        f.write(SEPA)
        
def writevals(f,i:int,e : MONELEM) :
    for l in e.vals :
        f.write(SEPA + l[i])

# --------------
# columns
# --------------  

LEFTM=1

def writeleft(f) :
    for _ in range(LEFTM) :
        f.write(SEPA)
        
def writeC(f,s):
    f.write(s + SEPA)
    
def writenl(f) :
    f.write("\n")    
        
def writelabels(f,e : MONELEM) :
    writeleft(f)
    for l in e.labels : writeC(f,l)
    writenl(f)
    
def writevalscol(f,envname : str, e : MONELEM) :
    writenl(f)
    writeC(f,envname)
    writenl(f)

    for l in e.vals :
        writeleft(f)
        for v in l :
            writeC(f,v)
        writenl(f)

class DB2MON : 
     
    def __init__(self,fname : str, envname:str) :
        self.fname :str = fname
        self.elem : MONELEM = None
        self.para : str = None
        self.envname : str = envname
        
    def toCVSCol(self,outfile: str, args: List[any]) :
        logging.info("Writing {0} to {1}".format(self.para,self.fname))
        with open(outfile,"w") as f :
            writelabels(f,self.elem)
            writevalscol(f,self.envname,self.elem)
            for m in args :
                writevalscol(f,m.envname,m.elem)
        
    def toCVS(self,outfile: str, args: List[any]) :
        logging.info("Writing {0} to {1}".format(self.para,self.fname))
        with open(outfile,"w") as f :
            writenl(f)
            
            f.write(SEPA+self.envname)
            writeempty(f,self.elem);            
              
            for k in args :
                writebetween(f)
                f.write(k.envname)
                writeempty(f,k.elem)
                
            f.write("\n\n\n")
                                               
            for i in range(0,len(self.elem.labels)) :
                f.write(self.elem.labels[i])
                writevals(f,i,self.elem)
                for k in args :
                    writebetween(f)
                    writevals(f,i,k.elem)
                    
                writenl(f)
        
        
    def read(self) :
        logging.info("Reading files: {0}".format(self.fname))
        with open(self.fname,'r') as f :
            self.lines = f.readlines()
        logging.info("{0} lines read".format(len(self.lines)))
            
    def tranformpar(self,par:str) :
        logging.info("Look for {0} in {1}".format(par,self.fname))
        prevl: str = None
        l : str
        state: int = 0
        labels : List[str] = None
        vals : List[List[str]] 
        
        self.para = par
        
        
        # 0 : outside, 1 : par found, 2: inside reading par
              
        for l in self.lines :
            if state == 0 :
                if l.rfind(par) != -1 :
                    logging.info("{0} found".format(par))
                    state = 1
            elif state == 1 :
                if l.startswith(MARKER) :
                    assert(prevl != None)
                    # prevl contains header, list of labels
                    logging.info("Read list of columns")
                    labels = transfortolist(prevl,[])
                    state = 2
                    vals = []
                    
                else : prevl = l
            else :
                assert(state == 2)
                if len(l.strip()) != 0 :
                    values = transfortolist(l,labels)
                    if len(values) != len(labels) :
                        logging.info(labels)
                        logging.info(l)
                        logging.info(values)
                        msg : str = "Number of labels {0} does not match number of values {1}".format(len(labels),len(values))
                        logging.critical(msg)
                        raise Exception(msg)
                    logging.info("Read line with results")
                    vals.append(values)
                else : 
                    self.elem = MONELEM(labels=labels,vals=vals)
                    return
                
        errmess : str = "{0} cannot be found in {1}".format(par,self.fname)
        logging.critical(errmess)
        raise Exception(errmess)
