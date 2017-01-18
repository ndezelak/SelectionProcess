@echo off
echo "------------Running algortihm-------------------"
python main.py
pause
cd Output\
echo "------------Deleting old PDFs-------------------"
for /r %%a in (Students_pdfs\*.pdf) do del "%%a"
echo "------------Generating new PDFs-------------------"
for /r %%v in (Students\*.html) do wkhtmltopdf "%%v" "Students_pdfs\%%~nv.pdf"

PAUSE