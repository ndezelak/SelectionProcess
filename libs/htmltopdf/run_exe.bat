@echo off
if not exist "%CD%\Output" mkdir "%CD%\Output"
if not exist "%CD%\Input" xcopy ("%CD%\..\htmltopdf\Input") ("%CD%") /E
if not exist "%CD%\Output\Students" mkdir "%CD%\Output\Students"
if not exist "%CD%\Output\Students_pdfs" mkdir "%CD%\Output\Students_pdfs"
if not exist "%CD%\Output\Global_pdfs" mkdir "%CD%\Output\Global_pdfs"
echo "------------ Deleting old HTMLs----------------"
for /r %%a in (Output\Students\*.html) do del "%%a"
for /r %%a in (Output\*.html) do del "%%a"
echo "------------Running algortihm-------------------"
main.exe
cd Output\
echo "------------Deleting old PDFs-------------------"
for /r %%a in (Students_pdfs\*.pdf) do del "%%a"
for /r %%a in (Global_pdfs\*.pdf) do del "%%a"
echo "------------Generating new PDFs-------------------"
echo "%CD%\Students_pdfs\"
for /r %%v in (Students\*.html) do wkhtmltopdf "%%v" "%CD%\Students_pdfs\%%~nv.pdf"
echo "------------ Generating global PDFs ---------"
for %%v in (Global\*.html) do wkhtmltopdf --page-size A4 -O Landscape "%%v" "%CD%\Global_pdfs\%%~nv.pdf"
REM for /r %%a in (*.html) do del "%%a"
PAUSE