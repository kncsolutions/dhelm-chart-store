set root=C:\Users\pallav\Anaconda3
call %root%\Scripts\activate.bat %root%
call conda list pandas
pause
py kite_instrument_list_dumper.py
pause