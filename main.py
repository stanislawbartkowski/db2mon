from util.readmon import DB2MON 
from typing import List,Tuple

import logging
logging.basicConfig(level=logging.INFO)

import os

FNAME1="/home/sbartkowski/work/repo/zreport-partitioned.out"
ENV1="LinuxOne"
FNAME2="/home/sbartkowski/work/repo/thinkde_xml_inline_rep.out"
ENV2="Laptop"


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


def createC(par:str, sheet:str) :
       
   M1 = DB2MON(FNAME1,ENV1)
   M1.read()
   M1.tranformpar(par)
   M2 = DB2MON(FNAME2,ENV2)
   M2.read()
   M2.tranformpar(par)
   M1.toCVS(os.path.join(OUTDIR,sheet),M2)
   
def createA() :
   for par,sheet in para : createC(par,sheet)
            

def main():
   print("Hello") 
#   createC(PAR4,SHEET4)
   createA()

if __name__ == "__main__":
    main()