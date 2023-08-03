# 2023. 07. 26.
# OpenVSP Batch Program ver. 2.1.0
# Main Code Developer   : Choi Inseo
# Sub Code Developer    : Shin Jinho 

import time
start = time.time()

from math import pi, atan, radians
import numpy as np

from InputDB            import LoadDB, ReqThrust
from AnalysisCondition  import DefineSetting, DefineLog
from ParamSetting       import CaseChecker, ClearPath, ParamMaker, RotationMaker
from PreProcess         import MakeCSV, MakeVSPAERO
from Solver             import ClearLog, CreateLog, RunVSPAERO, Post_1, Post_2

# ----------------------------------------------------------------------
#   경로 설정
# ----------------------------------------------------------------------

Path_DB             = 'C:\WORKINGSPACE\OpenVSP\AERODB'
Path_Geom           = 'C:\WORKINGSPACE\OpenVSP\AERODB\Geometry\VSP'
Path_Prop           = 'C:\WORKINGSPACE\OpenVSP\AERODB\Geometry\PropellerDB'
Path_Results        = 'C:\WORKINGSPACE\OpenVSP\AERODB\Results'
Path_Solver         = 'C:\WORKINGSPACE\OpenVSP\OpenVSP-3.30.0-win64\\vspaero.exe -omp 2 '

# ----------------------------------------------------------------------
#   항공기 형상 정보 로드
# ----------------------------------------------------------------------
"""
Aircraft List

KARI        : OPPAV
NASA        : Tilt_Wing / X57
WISK        : Cora
KittyHawk   : Heaviside
Joby        : S4
Chunbuk     : UAM
AEROLAB     : Model 1

Propeller List

Beaver      : Beaver
APC         : apce_9x6_rd0988_4003 / apce_10x7_pg0812_4007 / apcsf_10x4.7_kt0836_4014
"""
# Select the Geomety
Select_Geometry             = 'X57'
Select_Propeller            = 'Beaver', 'Beaver'
Save_Title                  = 'CIS_0726'

WingGeomDB, WingInitData    = LoadDB(Select_Geometry, Path_DB)

# ----------------------------------------------------------------------
#   해석 조건 설정
# ----------------------------------------------------------------------
Num_Panel                                   = 120                   # 격자 개수
Margin_Fuse                                 = 0.15                  # Ratio of the Fulelage width about wing span   default : 0.15
Margin_Disk                                 = 5                     # Margin = Semi_b / (Margin_Disk * NumP)        default : 5
Disk_XposiRatio                             = 1                     # Lx / MAC  (Mean Aerodynamic Chordlength)
Disk_ZposiRatio                             = 0                     # Lz / MAC  (Disk Diameter)

Analysis_AOA_Range                          = [4, 4, 1]             # [start, end, interval]
Analysis_Beta_Range                         = [0, 0, 1]             # [start, end, interval]
Analysis_Prop_Range                         = [2, 2, 1]             # [start, end, interval]

Analysis_T_Req, Density                     = ReqThrust(WingGeomDB, WingInitData)
INPUT_Analysis                              = DefineSetting(Analysis_AOA_Range, Analysis_Beta_Range,Analysis_Prop_Range,
                                                            Analysis_T_Req,
                                                            Path_Prop, Select_Propeller,
                                                            Num_Panel, Margin_Fuse, Margin_Disk,
                                                            Disk_XposiRatio, Disk_ZposiRatio)      
LogOutput                                   = DefineLog(Path_Results, Select_Geometry,
                                                        Select_Propeller, INPUT_Analysis,
                                                        Save_Title, WingGeomDB)

# ----------------------------------------------------------------------
#   모드 설정
# ----------------------------------------------------------------------

# Case Type
# 1: WTP no fixing
# 2: WTP fixing
Case =                      2
# Mode Type
# 1: Equal Spacing
# 2: Unequal Spacing-Left
# 3: Unequal Spacing-Center
# 4: Unequal Spacing-Right
Mode =                      3

# ----------------------------------------------------------------------
#   함수 설정
# ----------------------------------------------------------------------

# CASE GENERATOR
CaseChecker(Case, Mode, Analysis_Prop_Range)
GeneFolder = ClearPath(LogOutput, Case, Mode)
ParamMaker(GeneFolder, WingGeomDB, INPUT_Analysis, Case, Mode, Path_Prop, Select_Propeller, Density, Analysis_T_Req)
RotationMaker(GeneFolder, Analysis_Prop_Range, Mode, Case)

# PRE-PROCESSING VSPAERO
MakeCSV(Case, Mode, GeneFolder, Analysis_Prop_Range, Select_Geometry, Path_Geom)
MakeVSPAERO(Case, Mode, GeneFolder, Analysis_Prop_Range, Select_Geometry, Path_Geom,
            INPUT_Analysis, WingGeomDB)

# SOLVE-POST VSPAERO
ClearLog(GeneFolder, Case, Mode)
CreateLog(GeneFolder, Case, Mode, Analysis_Prop_Range)
RunVSPAERO(Path_Solver, GeneFolder, Case, Mode)
Post_1(GeneFolder, Case, Mode)
Post_2(GeneFolder, Case, Mode)

print("----------------------------------------------------------------------")
end = time.time()
print(f" 소요 시간 : {end - start:.5f} 초")