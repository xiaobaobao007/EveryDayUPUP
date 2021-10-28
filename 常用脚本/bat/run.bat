@echo off
set _lib=
set _path=libs
setlocal enabledelayedexpansion
for %%i in (%_path%/*.jar) do (
    set _lib=!_lib!%_path%/%%i;
)
rem run
"%JAVA_HOME%\bin\java" -server -Xmx512m -Xms256m -Xmn128m -cp %_lib%;resources; com.intion.App
rem debug
rem "%JAVA_HOME%\bin\java" -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 -server -Xmx512m -Xms256m -Xmn128m -cp %_lib%;resources; com.intion.App

pause