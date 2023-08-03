
import time
start = time.time()

from math import pi
import numpy as np

from ParamSetting import CaseChecker
from ParamSetting import ClearPath1
from ParamSetting import CallPropDB
from ParamSetting import FindSettting
from ParamSetting import FindSettting2
from ParamSetting import ParamMaker
from ParamSetting import RotationMaker

from PreProcess import MakeCSV
from PreProcess import MakeVSPAERO

from Solver import ClearLog
from Solver import CreateLog
from Solver import RunVSPAERO
from Solver import Post_1
from Solver import Post_2

#---------------------------------PATH-------------------------------------------#

FilePath =                  'C:\WORKINGSPACE\OpenVSP\PWI4\Geometry'
Filename =                  'Ge2_DegenGeom'
SLV_CMDPath =               'C:\WORKINGSPACE\OpenVSP\OpenVSP-3.30.0-win64\\vspaero.exe -omp 2 '
PropDB =                    'C:\WORKINGSPACE\OpenVSP\PWI4\Geometry\PropDB\Beaver'

# #---------------------------------INPUT-------------------------------------------#

# Wing Setting
b =                         7           # m
c_aero =                    1           # m
PropPosi_X =                -0.3
PropPosi_Z =                0
NumPanel =                  200
dy =                        (b/2) / NumPanel
L_Start =                   0.4170

# Reference Setting
# Baseline: Seo
AOA_Min =                   4               # deg.
AOA_Max =                   4               # deg.
AOA_Num =                   1               # deg.
AOA_List =                  list(np.linspace(AOA_Min, AOA_Max, AOA_Num))

Ref_D =                     1.5   # m
Ref_Hub =                   Ref_D * 0.2
Ref_Vinf =                  44.44   # m/s
Ref_Rho =                   1.225
Ref_RPM =                   1650
Ref_J =                     Ref_Vinf / ((Ref_RPM/60) * Ref_D)

Ref_Ct =                    CallPropDB(PropDB, Ref_J)[2]
Ref_Cp =                    CallPropDB(PropDB, Ref_J)[3]
Ref_T =                     Ref_Ct * 1.225 * (Ref_RPM/60)**2 * Ref_D**4
print(Ref_T)

# Semi-span based
Ref_NumProp =               2
Ref_T =                     Ref_NumProp * Ref_Ct * 1.225 * (Ref_RPM/60)**2 * Ref_D**4
Ref_TotalDisk =             Ref_NumProp * ((pi * Ref_D**2) / 4)

MinProp = 2
MaxProp = 7
#---------------------------------MODE SELECTION------------------------------------------#

# Case Type
# 1: WTP no fixing
# 2: WTP fixing
Case =                      1
# Mode Type
# 1: Equal Spacing
# 2: Unequal Spacing-Center
# 3: Unequal Spacing-Left
# 4: Unequal Spacing-Right
Mode =                      1

#-----------------------------------------------------------------------------------------#

#--------------------------------PARAMETER CREATOR----------------------------------------#
CaseChecker(Case, Mode, Ref_D, b, Ref_TotalDisk, MinProp, MaxProp)
ClearPath1(FilePath, Case, Mode)
ParamMaker(FilePath,Case, Mode, MinProp, MaxProp, PropDB, Ref_Hub, Ref_D, Ref_Vinf, Ref_J, b, Ref_T, dy, Ref_Rho)
# # RotationMaker(FilePath, MinProp, MaxProp, Mode, Case)

# # #-----------------------------------------------------------------------------------------#

# # #------------------------------PRE-PROCESSING VSPAERO-------------------------------------#

# # # MakeCSV(Case, Mode, FilePath, MaxProp, MinProp, Filename)
# # MakeVSPAERO(AOA_List, Case, Mode, MinProp, MaxProp, PropPosi_X, PropPosi_Z, FilePath, Ref_Ct, Ref_Cp, Ref_TotalDisk,
# #                 Ref_Hub, Ref_D, Ref_Vinf, Ref_J, Filename)

# #-----------------------------------------------------------------------------------------#

# #-----------------------------------SOLVE-POST VSPAERO-----------------------------------------#

# # ClearLog(FilePath, Case, Mode)
# # CreateLog(FilePath, Case, Mode, MinProp, MaxProp)
# # RunVSPAERO(SLV_CMDPath, FilePath, Case, Mode)
# # Post_1(FilePath, Case, Mode)
# # Post_2(FilePath, Case, Mode)

# #-----------------------------------------------------------------------------------------#
# end = time.time()
# print(f"{end - start:.5f} sec")