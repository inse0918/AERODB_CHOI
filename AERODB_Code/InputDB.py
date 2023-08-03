import os
import numpy as np

# ----------------------------------------------------------------------
#   INPUT : Gas Condition
# ----------------------------------------------------------------------

P       = 101.325       # 대기압
R       = 0.287         # 기체 상수
Temp    = 25            # 온도(섭씨)    

# ----------------------------------------------------------------------
#   INPUT 파일 형식
# ----------------------------------------------------------------------
"""
WingGeomDB File Format

    Span                = m
    Mean Chord          = m
    Root Chord          = m
    Tip Chord           = m
    Reference Area      = m**2
    Sweep Angle         = deg.
    Incidence Angle     = deg.
    Dihedral Angle      = deg.
    2nd Sweep Angle     = ratio
    Vinf                = m/s

WingInitData File Format

    Beta/Mach/AoA/Re/1e6/CL/CDo/CDi/CDtot/CDt/CDtot_t/CS/L/D/E/CFx/CFy/CFz/CMx/CMy/CMz/CMl/CMm/CMn/FOpt 
"""
#-----------------------------------------------Load DB-----------------------------------------------------------------#
def LoadDB(Select_Geometry, Path_DB):
    
    print("----------------------------------------------------------------------")
    print(" Selected Aircraft       : " + Select_Geometry)
    
    # 항공기 형상 정보 로드
    Path_GeomDB = Path_DB + '\\Geometry\\VSP\\' + Select_Geometry + '\\' + Select_Geometry + '.dat'
    data1 = np.loadtxt(Path_GeomDB)
    
    # 결과 파일 후처리
    File_lod = Path_DB + '\\Geometry\\VSP\\' + Select_Geometry + '\\' + Select_Geometry + '_DegenGeom.lod'
    File_hist = Path_DB + '\\Geometry\\VSP\\' + Select_Geometry + '\\' + Select_Geometry + '_DegenGeom.history'
    File_polar = Path_DB + '\\Geometry\\VSP\\' + Select_Geometry + '\\' + Select_Geometry + '_DegenGeom.polar'
    new_extension_lod = '_lod.dat'     
    new_extension_hist = '_hist.dat'     
    new_extension_polar = '_polar.dat'     
    change_file_extension(File_lod, new_extension_lod)
    change_file_extension(File_hist, new_extension_hist)
    change_file_extension(File_polar, new_extension_polar)
    
    # 공력 결과 로드
    
    Load_lod = Path_DB + '\\Geometry\\VSP\\' + Select_Geometry + '\\' + Select_Geometry + '_DegenGeom_polar.dat'
    data2 = np.genfromtxt(Load_lod, delimiter='')
    data2 = data2[1]
        
    return data1, data2


def change_file_extension(file_path, new_extension):
    
    # 파일 경로에서 파일 이름과 확장명 분리
    file_name, file_extension = os.path.splitext(file_path)

    # 새로운 확장명을 포함한 새로운 파일 이름 생성
    new_file_name = file_name + new_extension
    
    try:
        if os.path.exists(new_file_name):
            return
        else:
            os.rename(file_path, new_file_name)
    except OSError as e:
        print(f"파일 이름 변경에 실패했습니다: {e}")
        
    return False

# Required Thrust       = Aircraft Systemic Drag
# T_Req                 = D = CDtot(CDo + CDi) * q * S_ref

#-----------------------------------------------Cal Req Thrust-----------------------------------------------------------------#
def ReqThrust(WingGeomDB, WingInitData):
    
    rho = (P) / (R * (Temp+273))
    # Drag Calculation
    Vinf                = WingGeomDB[-1]
    Sref                = WingGeomDB[4]    
    CDtot               = WingInitData[7]
    
    T_Req               = (0.5 * rho * Vinf**2 ) * Sref * CDtot    
    
    print(" Required Thrust         : " + str(T_Req) + " [N]")
    
    return T_Req, rho
