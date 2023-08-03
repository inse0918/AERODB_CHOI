
from math import pi, sqrt, ceil
import os
import shutil
import glob
from AnalysisCondition  import check_and_create_folder

#-----------------------------------------------Clear Path-----------------------------------------------------------------#
def ClearPath(FilePath, Case, Mode):
     
    NewPath = 'Case' + str(Case) + 'Mode' + str(Mode)
    
    GeneFolder_init = FilePath + '\\' + NewPath
    
    check_and_create_folder(GeneFolder_init)
    
    GeneFolder = FilePath + '\\' + NewPath
    Remove_csv = GeneFolder + '\\' + '*.*'
    # [os.remove(f) for f in glob.glob(Remove_csv)]
    print(' ---  Path was Cleared    ---')
    
    # delete *.txt file
    Del_file_list = os.listdir(GeneFolder_init)
    # for file_name in Del_file_list:
    #     if file_name.startswith("Log_Case"):
    #         file_path = os.path.join(GeneFolder_init, file_name)
    #         os.remove(file_path)
    
    print(' ---  *.txt was Cleared   ---\n')
    return GeneFolder

#-----------------------------------------------Param Maker-----------------------------------------------------------------#    
def ParamMaker(FilePath, WingGeomDB, INPUT_Analysis, Case, Mode, Path_Prop, Select_Propeller, Density, Analysis_T_Req):
    
    ReadPropFile = Path_Prop + '\\' + Select_Propeller[0] + '\\' + Select_Propeller[1] + '.dat'
    NumProp = INPUT_Analysis[2][0]   # Init Prop Number    
    Min = (INPUT_Analysis[2][0])
    Max = (INPUT_Analysis[2][-1] + 1)

    NumPropList = list(range(int(Min), int(Max)))

    if Case == 1:       

            # Confirmed : Total System Thrust / No. of Disk is same with Total System Area / No. of Disk
            # NumU = 201, NumPANEL = 200, [dy = semispan / NumPANEL]
            # Constraints also function dy<Function of the number of panel>

        for i in range(0, len(NumPropList)):
            NumProp = NumPropList[i]
            print(' The Number of the Prop is : ' + str(NumProp))      
            DataInfo = [0] * (7 + NumProp)
            CaseName = 'Case' + str(Case) + '_' + str(NumProp)
            DataInfo[0] = CaseName
            DataInfo[1] = NumProp
            
            Semispan = WingGeomDB[0]/2
            TotT = INPUT_Analysis[3]
            dy = Semispan / INPUT_Analysis[6]
            PolyFitData = PropPolyfit(ReadPropFile)
            Semi_SysT   = TotT / 2
            Semi_Avail  = Semispan - (WingGeomDB[0] * INPUT_Analysis[7]) / 2
            
            
            SettingList = SolveDisk(Semi_SysT, Semispan, Semi_Avail, PolyFitData, WingGeomDB, Density, NumProp, Case)

            PropDiameter = SettingList[0]
            PropHub = PropDiameter * 0.2
            PropRPM = (SettingList[1])
            CT = (SettingList[2])
            CP = (SettingList[3])
            DataInfo[2] = PropDiameter 
            DataInfo[3] = PropHub
            DataInfo[4] = PropRPM
            DataInfo[5] = float(CT)
            DataInfo[6] = float(CP)

            T = Density * CT * ((PropRPM/60)**2) * PropDiameter**4
            print(f"    Precalculated  Thrust (Semi) : {round(Analysis_T_Req/2, 3)}")
            print(f"    Calculated     Thrust (Semi) : {round(NumProp*T, 3)}\n")
            
            multiplier = dy
            # EQUAL
            if Mode == 1:
                Yav = SettingList[4]
                Gap = SettingList[5]    
                FirstPropPosi = SettingList[6] + Gap + (PropDiameter / 2)
                RoundedFirstPropPosi = round(round(FirstPropPosi / multiplier) * multiplier, 5)
                DataInfo[7] = RoundedFirstPropPosi    
                PropPosi = RoundedFirstPropPosi
                # Propeller Position
                for k in range(0, NumProp-1):
                    PropPosi = PropPosi + Gap + (PropDiameter)
                    rounded_value = round(round(PropPosi / multiplier) * multiplier, 5)
                    PropPosi = rounded_value
                    DataInfo[8+k] = PropPosi
                InputData1Path = FilePath + '\\Case1_' + str(NumProp) + '.dat'

            # UNEQUAL - LEFT
            elif Mode == 2:
                FirstPropPosi = SettingList[6] + (PropDiameter / 2)
                RoundedFirstPropPosi = round(round(FirstPropPosi / multiplier) * multiplier, 5)
                DataInfo[7] = RoundedFirstPropPosi       
                PropPosi = RoundedFirstPropPosi
                for k in range(0, NumProp-1):
                    PropPosi = PropPosi + PropDiameter
                    rounded_value = round(round(PropPosi / multiplier) * multiplier, 5)
                    PropPosi = rounded_value               
                    DataInfo[8+k] = PropPosi
                InputData1Path = FilePath + '\\Case1_' + str(NumProp) + '.dat'
                
            # UNEQUAL - CENTER
            elif Mode == 3:
                SemiSpan_CNT = round(SettingList[6] + ((Semispan) - SettingList[6]) / 2, 5)
                DiaLength = NumProp * PropDiameter
                Dia_CNT_Posi = SettingList[6] + round(DiaLength / 2 , 5)
                L_CNT = round(SemiSpan_CNT - Dia_CNT_Posi , 5)   # Center of an Semi-span
                FirstPropPosi = SettingList[6] + L_CNT + (PropDiameter / 2)
                RoundedFirstPropPosi = round(round(FirstPropPosi / multiplier) * multiplier, 5)
                DataInfo[7] = RoundedFirstPropPosi 
                PropPosi = RoundedFirstPropPosi  
                # Propeller Position
                for k in range(0, NumProp-1):
                    PropPosi = PropPosi + PropDiameter
                    rounded_value = round(round(PropPosi / multiplier) * multiplier, 5)
                    PropPosi = rounded_value               
                    DataInfo[8+k] = PropPosi
                InputData1Path = FilePath + '\\Case1_' + str(NumProp) + '.dat'
            
            # UNEQUAL - RIGHT
            elif Mode == 4:
            
                DiaLength = NumProp * PropDiameter
                DataInfo[-1] = (Semispan)
                PropPosi = (Semispan)
                for k in range(0, NumProp-1):
                    PropPosi = PropPosi - PropDiameter
                    rounded_value = round(round(PropPosi / multiplier) * multiplier, 5)      
                    PropPosi = rounded_value
                    DataInfo[-k-2] = PropPosi
                InputData1Path = FilePath + '\\Case1_' + str(NumProp) + '.dat'        
            
            with open(InputData1Path, 'a') as f:
                    f.write(str(DataInfo))
                    f.write('\n')
            

    elif Case == 2:        
        for i in range(0, len(NumPropList)):
            
            NumProp = NumPropList[i]
            print(' The Number of the Prop is : ' + str(NumProp))      
            DataInfo = [0] * (7 + NumProp)
            CaseName = 'Case' + str(Case) + '_' + str(NumProp)
            DataInfo[0] = CaseName
            DataInfo[1] = NumProp
                        
            Semispan = WingGeomDB[0]/2
            TotT = INPUT_Analysis[3]
            dy = Semispan / INPUT_Analysis[6]
            PolyFitData = PropPolyfit(ReadPropFile)
            Semi_SysT   = TotT / 2
            Semi_Avail  = Semispan - (WingGeomDB[0] * INPUT_Analysis[7]) / 2
            
            SettingList2     = SolveDisk(Semi_SysT, Semispan, Semi_Avail, PolyFitData, WingGeomDB, Density, NumProp, Case)
            
            PropDiameter = SettingList2[0]
            PropHub = (PropDiameter) * 0.2
            PropRPM = SettingList2[1]
            CT = SettingList2[2]
            CP = SettingList2[3]
            
            WTPDiameter = SettingList2[7]
            WTPHubDiameter = WTPDiameter * 0.2
            WTPRPM      = SettingList2[8]
            WTPCT      = SettingList2[9]
            WTPCP      = SettingList2[10]
            
            DataInfo[2] = (PropDiameter, WTPDiameter) 
            DataInfo[3] = (PropHub, WTPHubDiameter)
            DataInfo[4] = (PropRPM, WTPRPM)
            DataInfo[5] = (float(CT), float(WTPCT))
            DataInfo[6] = (float(CP), float(WTPCP))                

            multiplier = dy

            if Mode == 1:
                Yav = DataInfo[4]
                Gap = SettingList2[5] / (NumProp)    
                FirstPropPosi = SettingList2[6] + Gap + (PropDiameter / 2)
                RoundedFirstPropPosi = round(round(FirstPropPosi / multiplier) * multiplier, 5)
                DataInfo[7] = RoundedFirstPropPosi      
                PropPosi = RoundedFirstPropPosi                # Propeller Position
                            
                for k in range(0, NumProp-1):
                    if k == NumProp-2:
                        DataInfo[8+k] = WingGeomDB[0]/2
                    else:
                        PropPosi = PropPosi + Gap + (PropDiameter)
                        rounded_value = round(round(PropPosi / multiplier) * multiplier, 5)
                        DataInfo[8+k] = rounded_value
                InputData1Path = FilePath + '\\Case2_' + str(NumProp) + '.dat' 

            elif Mode == 2:        
                FirstPropPosi = SettingList2[6] + (PropDiameter / 2)
                RoundedFirstPropPosi = round(round(FirstPropPosi / multiplier) * multiplier, 5)
                DataInfo[7] = RoundedFirstPropPosi       
                PropPosi = RoundedFirstPropPosi                
                for k in range(0, NumProp-1):
                    PropPosi = PropPosi + PropDiameter + multiplier/2
                    rounded_value = round(round(PropPosi / multiplier) * multiplier, 5)
                    PropPosi = rounded_value               
                    DataInfo[8+k] = PropPosi
                DataInfo[-1] = WingGeomDB[0]/2
                InputData1Path = FilePath + '\\Case2_' + str(NumProp) + '.dat' 
                
            elif Mode == 3:
                SemiSpan_CNT = round(SettingList2[6] + (WingGeomDB[0]/2 - (WTPDiameter/2) - SettingList2[6]) / 2, 5)                
                print(SemiSpan_CNT)
                DiaLength = (NumProp-1) * PropDiameter
                Dia_CNT_Posi = SettingList2[6] + round(DiaLength / 2 , 5)
                L_CNT = round(SemiSpan_CNT - Dia_CNT_Posi , 5)   # Center of an Semi-span                
                # Propeller Position
                FirstPropPosi = SettingList2[6] + L_CNT + (PropDiameter / 2)
                RoundedFirstPropPosi = round(round(FirstPropPosi / multiplier) * multiplier, 5)
                DataInfo[7] = RoundedFirstPropPosi 
                PropPosi = RoundedFirstPropPosi  
                
                for k in range(0, NumProp-1):
                    PropPosi = PropPosi + PropDiameter + multiplier/2
                    rounded_value = round(round(PropPosi / multiplier) * multiplier, 5)
                    PropPosi = rounded_value               
                    DataInfo[8+k] = PropPosi
                DataInfo[-1] = WingGeomDB[0]/2
                InputData1Path = FilePath + '\\Case2_' + str(NumProp) + '.dat' 

            elif Mode == 4:
                SemiSpan = WingGeomDB[0]/2
                DiaLength = (NumProp-1) * PropDiameter
                L_avail = SemiSpan - DiaLength
                PropPosi = WingGeomDB[0]/2
                PropPosi1 = PropPosi - WTPDiameter/2 - multiplier/2 - PropDiameter/2 - multiplier/2
                rounded_value = round(round(PropPosi1 / multiplier) * multiplier, 5) 
                DataInfo[-1] = PropPosi
                DataInfo[-2] = rounded_value
                for k in range(0, NumProp-2):
                    PropPosi = PropPosi1 - PropDiameter - multiplier/2
                    rounded_value = round(round(PropPosi / multiplier) * multiplier, 5)      
                    PropPosi1 = rounded_value
                    DataInfo[-k-3] = PropPosi1
                InputData1Path = FilePath + '\\Case2_' + str(NumProp) + '.dat'    

            with open(InputData1Path, 'a') as f:
                    f.write(str(DataInfo))
                    f.write('\n')
        print('Case' + str(Case) + '_' + str(NumProp))   
        print('[Case Input]: Data1 was Created')



#---------------------------------------------------Case Checker--------------------------------------------------------------#
def CaseChecker(Case, Mode, Analysis_Prop_Range):
    
    MinProp = Analysis_Prop_Range[0]
    MaxProp = Analysis_Prop_Range[1]
    
    print("----------------------------------------------------------------------")
    print(' Case : ' + str(Case))
    print(' Mode : ' + str(Mode))
    print(' MinProp : ' + str(MinProp))
    print(' MaxProp : ' + str(MaxProp))

    return

#-----------------------------------------------Rotation Maker-----------------------------------------------------------------#
def RotationMaker(FilePath, Analysis_Prop_Range, Mode, Case):
    import itertools
    
    MinProp = Analysis_Prop_Range[0]
    MaxProp = Analysis_Prop_Range[1]        
    NumPropList = list(range(MinProp, MaxProp+1))
    
    for i in range(0, len(NumPropList)):
        
        NumProp = NumPropList[i]
        Combi = []
        for perm in itertools.product("01", repeat=NumProp):
            Combi.append("".join(perm))
        combinations_result = Combi
        InputData1Path = FilePath + '\\Rot_Mode' +  str(Mode) + '_' + str(NumProp) + '.dat'
        with open(InputData1Path, 'w') as f:
            f.write(str(combinations_result))
            f.write('\n')
            
    print(' [Rotation Input]: Data2 was Created\n')
    return      

#-----------------------------------------------Find Solution-----------------------------------------------------------------#
def PropPolyfit(ReadPropFile):
    import numpy as np
    
    ReadPropFile = np.loadtxt(r"C:\WORKINGSPACE\OpenVSP\AERODB\Geometry\PropellerDB\Beaver\Beaver.dat")
    J = ReadPropFile[:, 0]
    CT = ReadPropFile[:, 1]
    CP = ReadPropFile[:, 2]

    Jran = np.arange(J[0], J[-1]+0.05, 0.05)
    PolyCT = np.polyfit(J, CT, 5)
    PolyCP = np.polyfit(J, CP, 5)
    
    PolyFitData = [PolyCT, PolyCP, Jran]
    
    return PolyFitData
    
def SolveDisk(Semi_SysT, Semi_b, Semi_Avail, PolyFitData, WingGeomDB, Density, NumProp, Case):
    
    if Case == 1:
   
        import numpy as np
        from scipy.optimize import fsolve
        
        # Num Prop
        NumP1_N = NumProp
        NumP1_SingleT = Semi_SysT / NumP1_N
        NumP1_Lstart = Semi_b - Semi_Avail
        NumP1_Margin = Semi_b / (5 * NumP1_N)
        NumP1_D = round(((Semi_Avail - (NumP1_N + 1) * NumP1_Margin) / NumP1_N), 8)
        NumP1_Gap = (Semi_Avail - (NumP1_D * NumP1_N)) / (NumP1_N + 1)
        
        C1, C2, C3, C4, C5, C6          = PolyFitData[0]
        Vinf = WingGeomDB[9]
        
        def equation(x):
            return (C1*x**5 + C2*x**4 + C3*x**3 + C4*x**2 + C5*x + C6) * (Vinf/(x*NumP1_D))**2 * (Density * NumP1_D**4) - NumP1_SingleT

        sol = fsolve(equation, 0.5)  # Using fsolve to find the roots of the equation

        CTSelect = float(np.polyval(PolyFitData[0], sol))
        CPSelect = float(np.polyval(PolyFitData[1], sol))
        nSelect = float((Vinf / (sol * NumP1_D)))
        RPMSelect = float(nSelect * 60)

        if sol > PolyFitData[2][-1]:
            print(f"\n  외삽법 영역입니다. J={sol}\n")
        else:
            print(f"\n  내삽법 영역입니다. J={sol}\n")

        SolveList = [NumP1_D, RPMSelect, CTSelect, CPSelect, Semi_Avail, NumP1_Gap, NumP1_Lstart]    
        
        return SolveList
    
    elif Case == 2:
        
        import numpy as np
        from scipy.optimize import fsolve
        C1, C2, C3, C4, C5, C6          = PolyFitData[0]
        Vinf = WingGeomDB[9]
        
        # Num Prop
        WTP_N = 1
        WTP_SingleT = (Semi_SysT / WTP_N) / 2
        WTP_Lstart = Semi_b - Semi_Avail
        WTP_Margin = Semi_b / (5 * WTP_N)
        WTP_D = round(((Semi_Avail - (WTP_N + 1) * WTP_Margin) / WTP_N), 8)
        
        def equation(x):
            return (C1*x**5 + C2*x**4 + C3*x**3 + C4*x**2 + C5*x + C6) * (Vinf/(x*WTP_D))**2 * (Density * WTP_D**4) - WTP_SingleT

        WTP_sol = fsolve(equation, 0.5)  # Using fsolve to find the roots of the equation

        WTPCTSelect = float(np.polyval(PolyFitData[0], WTP_sol))
        WTPCPSelect = float(np.polyval(PolyFitData[1], WTP_sol))
        WTPnSelect = float((Vinf / (WTP_sol * WTP_D)))
        WTPRPMSelect = float(WTPnSelect * 60)

        if WTP_sol > PolyFitData[2][-1]:
            print(f"\n  WTP : 외삽법 영역입니다. J={WTP_sol}\n")
        else:
            print(f"\n  WTP : 내삽법 영역입니다. J={WTP_sol}\n")              
        
        # Num Prop
        NumP1_N = NumProp - WTP_N
        NumP1_SingleT = (Semi_SysT - WTP_SingleT) / NumP1_N
        NumP1_Lstart = Semi_b - Semi_Avail
        NumP1_Margin = Semi_b / (5 * NumP1_N)
        NumP1_D = round(((Semi_Avail - (WTP_D/2) - (NumP1_N + 1) * NumP1_Margin) / NumP1_N), 8)
        NumP1_Gap = (Semi_Avail - (NumP1_D * NumP1_N)) / (NumP1_N + 1)
        
        def equation(x):
            return (C1*x**5 + C2*x**4 + C3*x**3 + C4*x**2 + C5*x + C6) * (Vinf/(x*NumP1_D))**2 * (Density * NumP1_D**4) - NumP1_SingleT

        sol = fsolve(equation, 0.5)  # Using fsolve to find the roots of the equation

        CTSelect = float(np.polyval(PolyFitData[0], sol))
        CPSelect = float(np.polyval(PolyFitData[1], sol))
        nSelect = float((Vinf / (sol * NumP1_D)))
        RPMSelect = float(nSelect * 60)

        if sol > PolyFitData[2][-1]:
            print(f"\n  IBP : 외삽법 영역입니다. J={sol}\n")
        else:
            print(f"\n  IBP : 내삽법 영역입니다. J={sol}\n")
            
        SolveList = [NumP1_D, RPMSelect, CTSelect, CPSelect, Semi_Avail, NumP1_Gap, NumP1_Lstart,
                     WTP_D, WTPRPMSelect, WTPCTSelect, WTPCPSelect]    
        
        return SolveList