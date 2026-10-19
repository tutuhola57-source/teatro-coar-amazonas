@echo off
chcp 65001 > nul
echo ============================================================
echo   PROCESADOR AUTOMATIZADO DE LIBRETOS - TEATRO COAR AMAZONAS
echo ============================================================
echo Escaneando Google Drive: G:\My Drive\Teatro_COAR_Buzon\Nuevos_Libretos_Para_Publicar...
echo.

cd /d "D:\Proyectos\teatro-coar-amazonas"
python scripts\procesar_buzon_drive.py

echo.
echo ============================================================
echo Proceso finalizado. Presione cualquier tecla para salir.
pause > nul
