# Microsoft Developer Studio Project File - Name="TUV42" - Package Owner=<4>
# Microsoft Developer Studio Generated Build File, Format Version 5.00
# ** DO NOT EDIT **

# TARGTYPE "Win32 (x86) Console Application" 0x0103

CFG=TUV42 - Win32 Debug
!MESSAGE This is not a valid makefile. To build this project using NMAKE,
!MESSAGE use the Export Makefile command and run
!MESSAGE 
!MESSAGE NMAKE /f "TUV42.mak".
!MESSAGE 
!MESSAGE You can specify a configuration when running NMAKE
!MESSAGE by defining the macro CFG on the command line. For example:
!MESSAGE 
!MESSAGE NMAKE /f "TUV42.mak" CFG="TUV42 - Win32 Debug"
!MESSAGE 
!MESSAGE Possible choices for configuration are:
!MESSAGE 
!MESSAGE "TUV42 - Win32 Release" (based on "Win32 (x86) Console Application")
!MESSAGE "TUV42 - Win32 Debug" (based on "Win32 (x86) Console Application")
!MESSAGE 

# Begin Project
# PROP Scc_ProjName ""
# PROP Scc_LocalPath ""
F90=df.exe
RSC=rc.exe

!IF  "$(CFG)" == "TUV42 - Win32 Release"

# PROP BASE Use_MFC 0
# PROP BASE Use_Debug_Libraries 0
# PROP BASE Output_Dir "Release"
# PROP BASE Intermediate_Dir "Release"
# PROP BASE Target_Dir ""
# PROP Use_MFC 0
# PROP Use_Debug_Libraries 0
# PROP Output_Dir "Release"
# PROP Intermediate_Dir "Release"
# PROP Target_Dir ""
# ADD BASE F90 /include:"Release/" /compile_only /nologo /warn:nofileopt
# ADD F90 /include:"Release/" /compile_only /nologo /warn:nofileopt
# ADD BASE RSC /l 0x809 /d "NDEBUG"
# ADD RSC /l 0x809 /d "NDEBUG"
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
LINK32=link.exe
# ADD BASE LINK32 kernel32.lib /nologo /subsystem:console /machine:I386
# ADD LINK32 kernel32.lib /nologo /subsystem:console /machine:I386

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

# PROP BASE Use_MFC 0
# PROP BASE Use_Debug_Libraries 1
# PROP BASE Output_Dir "Debug"
# PROP BASE Intermediate_Dir "Debug"
# PROP BASE Target_Dir ""
# PROP Use_MFC 0
# PROP Use_Debug_Libraries 1
# PROP Output_Dir "Debug"
# PROP Intermediate_Dir "Debug"
# PROP Target_Dir ""
# ADD BASE F90 /include:"Debug/" /compile_only /nologo /debug:full /optimize:0 /warn:nofileopt
# ADD F90 /include:"Debug/" /compile_only /nologo /debug:full /optimize:0 /warn:nofileopt
# ADD BASE RSC /l 0x809 /d "_DEBUG"
# ADD RSC /l 0x809 /d "_DEBUG"
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
LINK32=link.exe
# ADD BASE LINK32 kernel32.lib /nologo /subsystem:console /debug /machine:I386 /pdbtype:sept
# ADD LINK32 kernel32.lib /nologo /subsystem:console /debug /machine:I386 /pdbtype:sept

!ENDIF 

# Begin Target

# Name "TUV42 - Win32 Release"
# Name "TUV42 - Win32 Debug"
# Begin Source File

SOURCE=.\foil.for

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_FOIL_=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\functs.f
# End Source File
# Begin Source File

SOURCE=.\grids.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_GRIDS=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\la_srb.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_LA_SR=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\numer.f
# End Source File
# Begin Source File

SOURCE=.\odo3.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_ODO3_=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\odrl.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_ODRL_=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\orbit.f
# End Source File
# Begin Source File

SOURCE=.\rdetfl.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_RDETF=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\rdinp.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_RDINP=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\rdxs.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_RDXS_=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\rtrans.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_RTRAN=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\rxn.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_RXN_F=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\savout.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_SAVOU=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\setaer.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_SETAE=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\setalb.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_SETAL=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\setcld.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_SETCL=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\setno2.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_SETNO=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\seto2.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_SETO2=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\setso2.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_SETSO=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\sphers.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_SPHER=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\swbiol.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_SWBIO=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\swbiol2.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_SWBIOL=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\swbiol3.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_SWBIOL3=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\swchem.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_SWCHE=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\swphys.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_SWPHY=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\TUV42.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_TUV42=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\vpair.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_VPAIR=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\vpo3.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_VPO3_=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\vptmp.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_VPTMP=\
	".\params"\
	

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\wshift.f

!IF  "$(CFG)" == "TUV42 - Win32 Release"

!ELSEIF  "$(CFG)" == "TUV42 - Win32 Debug"

DEP_F90_WSHIF=\
	".\params"\
	

!ENDIF 

# End Source File
# End Target
# End Project
