import numpy as np
import os
import shutil

# Define the Analysis Condtion
# - Range of the AoA
# - Range of the Beta   ! 아직 적용 X
# - Reference Number of the Disk
# - Geometry of the Propeller


#-----------------------------------------------Analysis Condition-----------------------------------------------------------------#
def DefineSetting(Analysis_AOA_Range, Analysis_Beta_Range,Analysis_Prop_Range, Analysis_T_Req, Path_Prop, Select_Propeller,
                  Num_Panel, Margin_Fuse, Margin_Disk, Disk_XposiRatio, Disk_ZposiRatio):
    
    AoA_List                    = list(np.linspace(Analysis_AOA_Range[0], Analysis_AOA_Range[1], Analysis_AOA_Range[2]))
    Beta_List                   = list(np.linspace(Analysis_Beta_Range[0], Analysis_Beta_Range[1], Analysis_Beta_Range[2]))
    Prop_List                   = list(np.linspace(Analysis_Prop_Range[0], Analysis_Prop_Range[1], Analysis_Prop_Range[2]))
    Thurst_Semi                 = (Analysis_T_Req / 2)    # Semi-span에 할당하는 추력
    
    Prop_load                    = Path_Prop + '\\' + Select_Propeller[0] + '\\' + Select_Propeller[1] + '.dat'
    Prop_data = np.genfromtxt(Prop_load, delimiter='')     
    
    INPUT                       = [AoA_List, Beta_List, Prop_List, Analysis_T_Req, Thurst_Semi, Prop_data,
                                   Num_Panel, Margin_Fuse, Margin_Disk,
                                   Disk_XposiRatio, Disk_ZposiRatio]
    print(" Selected Propeller      : " + str(Select_Propeller[1]))
    
    return INPUT

"""
INPUT data format

AoA List
Beta List
Prop List
Total Thrust
Semi Thrust
Prop Data
Num Panel
Margin_Fuse
Margin_Disk
Disk_XposiRatio
Disk_ZposiRatio

"""
#-----------------------------------------------Defining Log-----------------------------------------------------------------#
def DefineLog(Path_Results, Select_Geometry, Select_Propeller, INPUT_Analysis, Save_Title, WingGeomDB):
    
    
    Path_Save   = Path_Results + '\\' + Save_Title + '_' + Select_Geometry
    Path_Log    = Path_Save + '\\' +  Select_Geometry + '_Log.dat'
    check_and_create_folder(Path_Save)
    
    save_to_dat_file(Path_Log, Select_Geometry, Select_Propeller, INPUT_Analysis, WingGeomDB)

    return Path_Save

def check_and_create_folder(folder_path):
    # 폴더가 존재하는지 확인
    if os.path.exists(folder_path):
        # 사용자로부터 입력 받기
        response = input(f"\n'{folder_path}'    해당 폴더가 존재합니다, 폴더를 삭제하시겠습니까? (Y/N): ").strip().upper()
        if response == 'Y':
            # 폴더 삭제
            try:
                shutil.rmtree(folder_path)
                print(f"\n'{folder_path}'    폴더를 삭제했습니다.")
            except OSError as e:
                print(f"\n'{folder_path}'    폴더를 삭제하는 도중 오류가 발생했습니다: {e}")
                return
            # 폴더 생성
            try:
                os.makedirs(folder_path)
                print(f"\n '{folder_path}'   폴더를 다시 생성했습니다.\n")
            except OSError as e:
                print(f"\n'{folder_path}'    폴더를 생성하는 도중 오류가 발생했습니다: {e}")
        elif response == 'N':
            print(f"\n'{folder_path}'    폴더를 삭제하지 않고 진행합니다.\n")
        else:
            print(f"\n'{folder_path}'    잘못된 입력입니다. 'Y' 또는 'N'을 입력해주세요.")
    else:
        # 폴더가 없는 경우, 폴더 생성
        try:
            os.makedirs(folder_path)
            print(f"\n{folder_path}'    폴더를 생성했습니다.\n")
        except OSError as e:
            print(f"\n{folder_path}'    폴더를 생성하는 도중 오류가 발생했습니다: {e}")

        
        
def save_to_dat_file(file_path, Select_Geometry, Select_Propeller, INPUT_Analysis, WingGeomDB):
    with open(file_path, 'w') as file:
        file.write(f'Selected Aircraft, {Select_Geometry}\n')
        file.write(f'Selected Propeller, {Select_Propeller}\n')
        file.write(f'Free Stream Velocity, {WingGeomDB[-1]}\n')
        file.write(f'AoA_List, {INPUT_Analysis[0]}\n')
        file.write(f'Beta List, {INPUT_Analysis[1]}\n')
        file.write(f'Prop List, {INPUT_Analysis[2]}\n')
        file.write(f'Requied Thrust, {INPUT_Analysis[3]}\n')
        file.write(f'Thrust[Semi-span], {INPUT_Analysis[4]}\n')





