from util.readmon import DB2MON 
from typing import List,Tuple

import logging
logging.basicConfig(level=logging.INFO)

import os

FNAME1="/home/sbartkowski/work/repo/zreport-partitioned.out"
ENV1="LinuxOne"
FNAME2="/home/sbartkowski/work/repo/thinkde_xml_inline_rep.out"
ENV2="Laptop"
files : List[Tuple[str,str]] = [(FNAME1,ENV1),(FNAME2,ENV2)]


PAR1="DB#THRUP: Throughput metrics at database level"
SHEET1="Throughput metrics at database level.csv"

PAR2="DB#TIMEB: Time breakdown at database level (wait + processing)"
SHEET2="Time breakdown at database level (wait + processing).csv"

PAR3="DB#WAITT: Wait times at database level"
SHEET3="Wait times at database level.csv"

PAR4="SQL#TOPEXECT: Top SQL statements by execution time"
SHEET4="Top SQL statements by execution time.csv"

PAR5="SQL#TOPWAITT: Wait time breakdown for top SQL statements by execution time"
SHEET5="Wait time breakdown for top SQL statements by execution time.csv"

PAR6="SQL#TOPIOSTA: IO statistics per stmt - top statements by execution time"
SHEET6="IO statistics per stmt - top statements by execution time.csv"

PAR7="DB#LOGWR: Database log write times"
SHEET7="Database log write times.csv"

PAR8="BPL#READS: Bufferpool read statistics (overall)"
SHEET8="Bufferpool read statistics (overall).csv"

PAR9="TSP#DSKIO: Disk read and write I/O times"
SHEET9="Disk read and write IO times.csv"

PAR10="LTC#WAITT: Latch wait metrics"
SHEET10="Latch wait metrics.csv"

OUTDIR="output"

para : List[Tuple[str,str]] = [(PAR1,SHEET1),(PAR2,SHEET2),(PAR3,SHEET3),(PAR4,SHEET4),(PAR5,SHEET5),(PAR6,SHEET6),(PAR7,SHEET7),(PAR8,SHEET8),(PAR9,SHEET9),(PAR10,SHEET10)]

files1 : List[Tuple[str,str]] = [(FNAME1,ENV1),(FNAME2,ENV2)]


MDIR="xxxx"

files2 : List[str] = ["db2mon2_120_1130.out","db2mon3_120_1140.out","db2mon4_120_1155.out","db2mon5_300_1220.out","db2mon6_300_1245.out", \
  "db2mon7_300_1310.out", "db2mon8_300_1340.out","db2mon9_300_1350.out","db2mon10_300_1425.out","db2mon11_300_1445.out", \
  "db2mon12_300_1505.out","db2mon13_300_1520.out","db2mon14_300_1555.out"]

def xxxcreateC(par:str, sheet:str) :
       
   M1 = DB2MON(FNAME1,ENV1)
   M1.read()
   M1.tranformpar(par)
   M2 = DB2MON(FNAME2,ENV2)
   M2.read()
   M2.tranformpar(par)
   M1.toCVS(os.path.join(OUTDIR,sheet),M2)
   
   
def createC(par:str, sheet:str,files : List[Tuple[str,str]]) :
   M1 : DB2MON = None
   MLIST : List[DB2MON] = []
   for fname,env in files :
      M = DB2MON(fname,env)
      M.read()
      M.tranformpar(par)
      if M1 is None : M1 = M
      else: MLIST.append(M)
      
   M1.toCVS(os.path.join(OUTDIR,sheet),MLIST)

   
def createA(files : List[Tuple[str,str]]) :
   for par,sheet in para : createC(par,sheet,files)
   
def createAA(inputdir: str, fnames:List[str]) :
   files : List[Tuple[str,str]] = []
   
   for f in fnames :
          filename=os.path.join(inputdir,f)
          env = os.path.splitext(f)[0]
          files.append((filename,env))
   createA(files)          
          
            

def main():
   print("Hello") 
#   createC(PAR4,SHEET4)
   #createA(files1)
   createAA(MDIR,files2)

if __name__ == "__main__":
    main()