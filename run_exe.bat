@echo off
echo "------------ Deleting old HTMLs----------------"
for /r %%a in (Students\*.html) do del "%%a"
echo "------------Running algortihm-------------------"
python main.py
cd Output\
echo "------------Deleting old PDFs-------------------"
for /r %%a in (Students_pdfs\*.pdf) do del "%%a"
echo "------------Generating new PDFs-------------------"
for /r %%v in (Students\*.html) do wkhtmltopdf "%%v" "Students_pdfs\%%~nv.pdf"
cd ..
for  %%v in (Global\*.html) do Output\wkhtmltopdf --page-size A3 -O Landscape "%%v" "Global_pdf\%%~nv.pdf"
PAUSE