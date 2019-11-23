set root=C:\Users\pallav\Anaconda3
call %root%\Scripts\activate.bat %root%
call conda list pandas
pause
py kite_chart_store_segment2.py
pause