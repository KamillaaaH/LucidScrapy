LucidScrapy
===========

This is a project about transparency and open government. It'll show expenses from 
Governo do Distrito Federal (Brazil) using detailed charts. That will be useful for citizens who want 
to check public expenses.
 
 --- Assigment (Report):
~/LucidScrapy/docs/relatorio/Relatorio_V.pdf

 --- Specifications:
Operational System - Ubuntu 11.04
Netbeans 6.5
Python 2.7.2
C Programming Language
Doxygen 1.8.2
Git distributed version control system 1.7.12

 --- Authors and Contributors:
Kamilla H. Crozara (@KamillaaaH) and Maylon Felix (@MaylonFelix).

 --- Home Page:
http://kamillaaah.github.com/LucidScrapy/

 --- Setup: 
It's under development so it needs some already instaled modules to execute. Before execute is necessary 
install manually:

* Mechanize - http://wwwsearch.sourceforge.net/mechanize/
* Ctypes - http://docs.python.org/library/ctypes.html

 --- Run:

Inside the paste ~/LucidScrapy/moduleVectorHash follow command bellow:

$ make compile

Inside the paste ~/LucidScrapy of the project follow command bellow:

$ python LucidScrapy.py


It'll get data from Portal da Transparência do Distrito Federal and store it inside CSV files. Sometimes it 
doesn't work because the Portal da Transparência do Distrito Federal could be temporary unavailable.


TODO:

* Get all data into CSV files and plot it using HighCharts.  