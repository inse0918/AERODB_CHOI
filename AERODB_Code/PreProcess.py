# VSPAERO PRE-PROCESSING

import os
import shutil
import pandas as pd
import csv
import numpy as np
import glob 
import os
from math import pi, sqrt

# GeneFolder : 생성할 폴더
# Path_Geom : 기존 VSP 파일 묶음이 있는 폴더

def ClearPath2(Case, Mode, FilePath):

    NewPath = 'Case' + str(Case) + 'Mode' + str(Mode)
    GeneFolder_init = FilePath + '\\' + NewPath
    if os.path.isdir(GeneFolder_init):
        shutil.rmtree(GeneFolder_init)            
    GeneFolder = FilePath + '\\' + NewPath
    os.mkdir(GeneFolder)
    GeneFolder = FilePath + '\\' + NewPath
    Remove_csv = GeneFolder + '\\' + '*.*'
    [os.remove(f) for f in glob.glob(Remove_csv)]
    print(' ---Path was Cleared---\n')
    return

def MakeCSV(Case, Mode, GeneFolder, Analysis_Prop_Range, Select_Geometry, Path_Geom):
    print(' ---Creating CSV Files...---\n')
    Filename = Select_Geometry + '_DegenGeom.csv'
    
    MinProp = Analysis_Prop_Range[0]
    MaxProp = Analysis_Prop_Range[1]
    FilePath = GeneFolder

    NumPropList = list(range(MinProp, MaxProp+1))     
    
    for i in range(0, len(NumPropList)):          
        NumProp = NumPropList[i]
        NumRot = 2 ** NumProp
        NumRotList = list(range(1, NumRot+1))
        
        source_folder = Path_Geom + '\\' + Select_Geometry  # 원본 파일이 있는 폴더 경로
        destination_folder = FilePath                        # 복사할 대상 폴더 경로
        
        for j in range(0, NumRot):
            NewName = 'C' + str(Case) + 'M' + str(Mode) + 'N' + str(NumProp) + 'R' + str(NumRotList[j]) + '.csv'            
            source_file_path = os.path.join(source_folder, Filename)
            destination_file_path = os.path.join(destination_folder, NewName)
            shutil.copy(source_file_path, destination_file_path)
        
    print(' [Notice]: CSV Files was Created\n')
    return

def MakeVSPAERO(Case, Mode, GeneFolder, Analysis_Prop_Range, Select_Geometry, Path_Geom,
            INPUT_Analysis, WingGeomD):
    import math
    print(' ---Creating VSPAERO Files...---')
    
    MinProp = Analysis_Prop_Range[0]
    MaxProp = Analysis_Prop_Range[1]
        
    SweptAng        = WingGeomD[5]
    SweptAngRatio   = WingGeomD[8]
    Span            = WingGeomD[0]
    Crt             = WingGeomD[2]
    Ctip            = WingGeomD[3]
    MAC             = WingGeomD[1]
    
    Ref_XPosi       = -(INPUT_Analysis[9] * MAC)
    Ref_ZPosi       = (INPUT_Analysis[10] * MAC)
    
    CrtPrime            = Crt - Ctip
    SemiB               = Span / 2
    CtipPosi            = CrtPrime * SweptAngRatio
    angle_rad = math.atan(CtipPosi / SemiB)
    SweptAngle          = math.degrees(angle_rad)
    SweptAngleValue     = math.tan(math.radians(SweptAng + SweptAngle))
        
    NewPath = 'Case' + str(Case) + 'Mode' + str(Mode)
    GeneFolder = GeneFolder
    NumPropList = list(range(MinProp, MaxProp+1))        
    # Read the Original VSPAERO
    Filename = Select_Geometry + '_DegenGeom.vspaero'    
    source_folder = Path_Geom + '\\' + Select_Geometry
    lodFile_vspaero = source_folder + '\\' + Filename  # 원본 파일이 있는 폴더 경로   
    with open(lodFile_vspaero, 'r') as file:    
            VSPAERO_Load = file.readlines()     
            
    for i in range(0, len(NumPropList)):     
        # Read the Input Datas
        Path_PropData = GeneFolder + '\\Rot_Mode' + str(Mode) + '_' + str(NumPropList[i]) + '.dat'
        Path_GeomData = GeneFolder + '\\Case' + str(Case) + '_' + str(NumPropList[i]) + '.dat'
        with open(Path_PropData, "r") as f:
            ReadRotData = str(f.readlines()).split(',')
        ReadRotData = [s.replace(']', '').replace('[', '').replace(',', '').replace('"', '').replace('\\n', '').replace("'", '') for s in ReadRotData]
        with open(Path_GeomData, "r") as f:
            ReadGeomData = str(f.readlines()).split(',')
        ReadGeomData = [s.replace(']', '').replace('[', '').replace(',', '').replace('"', '').replace('\\n', '').replace("'", '') for s in ReadGeomData]
        
        if  Case == 1:
            VSPAERO_D = float(ReadGeomData[2])
            VSPAERO_HubD = float(ReadGeomData[3])
            VSPAERO_RPM = float(ReadGeomData[4])
            CT = float(ReadGeomData[5])
            CP = float(ReadGeomData[6])

        elif Case == 2:
            VSPAERO_D = float(ReadGeomData[2].replace('(', ''))
            VSPAERO_HubD = float(ReadGeomData[4].replace('(', ''))
            VSPAERO_RPM = float(ReadGeomData[6].replace('(', ''))
            CT = float(ReadGeomData[8].replace('(', ''))
            CP = float(ReadGeomData[10].replace('(', ''))
            VSPAERO_WTPD = float(ReadGeomData[3].replace(')', ''))
            VSPAERO_WTPHubD = float(ReadGeomData[5].replace(')', ''))
            VSPAERO_WTPRPM = float(ReadGeomData[7].replace(')', ''))
            CT_WTP = float(ReadGeomData[9].replace(')', ''))
            CP_WTP = float(ReadGeomData[11].replace(')', ''))
        
        NumProp = NumPropList[i]
        NumRot = 2 ** NumProp

        if Case == 2:
            WTPDiameter = VSPAERO_WTPD
            WTPHub = VSPAERO_WTPHubD
            WTPRPM = VSPAERO_WTPRPM

        for j in range(0, NumRot):
            VSPAERO_Frnt = VSPAERO_Load[0:18]
            AOA_Range = 'AoA = ' + str(INPUT_Analysis[0]).replace('[','').replace(']','') + '\n'
            VSPAERO_Frnt[7] = AOA_Range
            VSPAERO_Bck = VSPAERO_Load[55:60]
            VSPAERO_PropSize = NumPropList[i] * 2
            VSPAERO_NumProp = 'NumberOfRotors = ' + str(VSPAERO_PropSize) + '\n'
            VSPAERO_Frnt.append(VSPAERO_NumProp)   
            NumRotList = list(str(ReadRotData[j]).strip())
            NewName = 'C' + str(Case) + 'M' + str(Mode) + 'N' + str(NumProp) + 'R' + str(j+1)

            if Case == 1:
                for k in range(0, len(NumRotList)):
                    Direct_Sel = int(NumRotList[k])
                    PropTitle1 = 'PropElement_' + str((k * 2) + 1)
                    PropPosi1 = str((Ref_XPosi + ((float(str(ReadGeomData[7 + k]).strip())) * SweptAngleValue ))) + \
                    ' ' + str(float(str(ReadGeomData[7 + k]).strip())) + ' ' + str(Ref_ZPosi)
                    
                    Index2 = '1.000000 0.000000 0.000000'                
                    PropTitle2 = 'PropElement_' + str((k + 1) * 2)
                    PropPosi2 = str((Ref_XPosi + ((float(str(ReadGeomData[7 + k]).strip())) * SweptAngleValue ))) + \
                    ' ' + str(-float(str(ReadGeomData[7 + k]).strip())) + ' ' + str(Ref_ZPosi)
                                    
                    # First 
                    VSPAERO_Frnt.append(PropTitle1 + '\n')
                    VSPAERO_Frnt.append(str((k * 2) + 1) + '\n')
                    VSPAERO_Frnt.append(PropPosi1 + '\n')
                    VSPAERO_Frnt.append(Index2 + '\n')
                    VSPAERO_Frnt.append(str((VSPAERO_D/2)) + '\n')
                    VSPAERO_Frnt.append(str(VSPAERO_HubD/2) + '\n')
                    if Direct_Sel == 0:
                        VSPAERO_Frnt.append(str(-VSPAERO_RPM) + '\n')
                    elif Direct_Sel == 1:
                        VSPAERO_Frnt.append(str(VSPAERO_RPM) + '\n')
                    VSPAERO_Frnt.append(str(CT) + '\n')
                    VSPAERO_Frnt.append(str(CP) + '\n')

                    # Next 
                    VSPAERO_Frnt.append(PropTitle2 + '\n')
                    VSPAERO_Frnt.append(str((k + 1) * 2) + '\n')
                    VSPAERO_Frnt.append(PropPosi2 + '\n')
                    VSPAERO_Frnt.append(Index2 + '\n')
                    VSPAERO_Frnt.append(str((VSPAERO_D/2)) + '\n')
                    VSPAERO_Frnt.append(str(VSPAERO_HubD/2) + '\n')
                    if Direct_Sel == 0:
                        VSPAERO_Frnt.append(str(VSPAERO_RPM) + '\n')
                    elif Direct_Sel == 1:
                        VSPAERO_Frnt.append(str(-VSPAERO_RPM) + '\n')
                    VSPAERO_Frnt.append(str(CT) + '\n')
                    VSPAERO_Frnt.append(str(CP) + '\n')
            
            if Case == 2:
                for k in range(0, len(NumRotList)):
                    Direct_Sel = int(NumRotList[k])
                    PropTitle1 = 'PropElement_' + str((k * 2) + 1)
                    PropPosi1 = str((Ref_XPosi + ((float(str(ReadGeomData[11 + k + 1]).strip())) * SweptAngleValue ))) + \
                    ' ' + str(float(str(ReadGeomData[11 + k + 1]).strip())) + ' ' + str(Ref_ZPosi)
                    
                    Index2 = '1.000000 0.000000 0.000000'                
                    PropTitle2 = 'PropElement_' + str((k + 1) * 2)
                    PropPosi2 = str((Ref_XPosi + ((float(str(ReadGeomData[11 + k + 1]).strip())) * SweptAngleValue ))) + \
                    ' ' + str(-float(str(ReadGeomData[11 + k + 1]).strip())) + ' ' + str(Ref_ZPosi)
                    # First 
                    VSPAERO_Frnt.append(PropTitle1 + '\n')
                    VSPAERO_Frnt.append(str((k * 2) + 1) + '\n')
                    VSPAERO_Frnt.append(PropPosi1 + '\n')
                    VSPAERO_Frnt.append(Index2 + '\n')
                    
                    if k == len(NumRotList)-1:
                        VSPAERO_Frnt.append(str((WTPDiameter/2)) + '\n')
                        VSPAERO_Frnt.append(str(WTPHub/2) + '\n')
                        if Direct_Sel == 0:
                            VSPAERO_Frnt.append(str(-WTPRPM) + '\n')
                        elif Direct_Sel == 1:
                            VSPAERO_Frnt.append(str(WTPRPM) + '\n')
                        VSPAERO_Frnt.append(str(CT_WTP) + '\n')
                        VSPAERO_Frnt.append(str(CP_WTP) + '\n')
                    else:
                        VSPAERO_Frnt.append(str((VSPAERO_D/2)) + '\n')
                        VSPAERO_Frnt.append(str(VSPAERO_HubD/2) + '\n')
                        if Direct_Sel == 0:
                            VSPAERO_Frnt.append(str(-VSPAERO_RPM) + '\n')
                        elif Direct_Sel == 1:
                            VSPAERO_Frnt.append(str(VSPAERO_RPM) + '\n')

                        VSPAERO_Frnt.append(str(CT) + '\n')
                        VSPAERO_Frnt.append(str(CP) + '\n')

                    # Next 
                    VSPAERO_Frnt.append(PropTitle2 + '\n')
                    VSPAERO_Frnt.append(str((k + 1) * 2) + '\n')
                    VSPAERO_Frnt.append(PropPosi2 + '\n')
                    VSPAERO_Frnt.append(Index2 + '\n')

                    if k == len(NumRotList)-1:
                        VSPAERO_Frnt.append(str((WTPDiameter/2)) + '\n')
                        VSPAERO_Frnt.append(str(WTPHub/2) + '\n')
                        if Direct_Sel == 0:
                            VSPAERO_Frnt.append(str(WTPRPM) + '\n')
                        elif Direct_Sel == 1:
                            VSPAERO_Frnt.append(str(-WTPRPM) + '\n')
                        VSPAERO_Frnt.append(str(CT_WTP) + '\n')
                        VSPAERO_Frnt.append(str(CP_WTP) + '\n')
                    else:
                        VSPAERO_Frnt.append(str((VSPAERO_D/2)) + '\n')
                        VSPAERO_Frnt.append(str(VSPAERO_HubD/2) + '\n')
                        if Direct_Sel == 0:
                            VSPAERO_Frnt.append(str(VSPAERO_RPM) + '\n')
                        elif Direct_Sel == 1:
                            VSPAERO_Frnt.append(str(-VSPAERO_RPM) + '\n')      

                        VSPAERO_Frnt.append(str(CT) + '\n')
                        VSPAERO_Frnt.append(str(CP) + '\n')

            VSPAERO_Frnt.extend(VSPAERO_Bck)
            VSPAERO_Results = VSPAERO_Frnt
            NewFilePath = GeneFolder +  "\\" + NewName + ".vspaero"
            f = open(NewFilePath, 'w')
            f.writelines((VSPAERO_Results))
            f.close()
            print(NewFilePath)
            
    print('\n   [Notice]: VSPAERO Files was Created\n')
    return

    
    
    
    
    
    
