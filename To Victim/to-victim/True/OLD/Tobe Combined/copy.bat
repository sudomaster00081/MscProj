@echo off

setlocal enabledelayedexpansion

rem Combine all CSV files into one
copy *.csv ddostrace.to-victim.20070804.csv

echo All files combined.

endlocal
