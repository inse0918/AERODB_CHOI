# VSPAERO SOLVER

#-----------------------------------------------Clear Log-----------------------------------------------------------------#
def ClearLog(FilePath, Case, Mode):
    print('---Clearing Log---')
    import os
    NewPath = 'Case' + str(Case) + 'Mode' + str(Mode)

    SLV_LogPath = FilePath + '\\' + '\\Log_' + NewPath + '.dat'

    if os.path.exists(SLV_LogPath):
        os.remove(SLV_LogPath)

    with open(SLV_LogPath, 'w') as f:
        pass    
    
    print('---Log was Cleared---')
    return

#-----------------------------------------------Create Log-----------------------------------------------------------------#
def CreateLog(GeneFolder, Case, Mode, Analysis_Prop_Range):
    
    MinProp = Analysis_Prop_Range[0]
    MaxProp = Analysis_Prop_Range[1]
    
    print('---Creating Log---')
    NewPath = 'Case' + str(Case) + 'Mode' + str(Mode)
    SLV_LogPath = GeneFolder + '\\' +  '\\Log_' + NewPath + '.dat'
    NumPropList = list(range(MinProp, MaxProp+1))   
    for i in range(0, len(NumPropList)):      
        NumProp = NumPropList[i]
        NumRot = 2 ** NumProp
        NumRotList = list(range(1, NumRot+1))
        Path_PropData = GeneFolder + '\\' + '\\Rot_Mode' + str(Mode) + '_' + str(NumPropList[i]) + '.dat'
        with open(Path_PropData, "r") as f:
            ReadRotData = str(f.readlines()).split(',')
        ReadRotData = [s.replace(']', '').replace('[', '').replace(',', '').replace('"', '').replace('\\n', '').replace("'", '') for s in ReadRotData]
    
        for j in range(0, NumRot):
            NewName = 'C' + str(Case) + 'M' + str(Mode) + 'N' + str(NumProp) + 'R' + str(NumRotList[j])
            RotData = ReadRotData[j].strip()
            SaveLogData = NewName + ' ' + RotData
            with open(SLV_LogPath, 'a') as f:
                f.write(SaveLogData)
                f.write('\n')
    
    print('---Log was Created---\n')
    return

#-----------------------------------------------Run VSPAERO------------------------------------------------------------#
def RunVSPAERO(SLV_CMDPath, FilePath, Case, Mode):
    print('---Running VSPAERO---')
    import os

    NewPath = 'Case' + str(Case) + 'Mode' + str(Mode)
    SLV_LogPath = FilePath + '\\' + '\\Log_' + NewPath + '.dat'
    
    
    
    with open(SLV_LogPath, 'r') as file:    
            SLV_LoadLog = file.readlines()
             
    for i in range(0, len(SLV_LoadLog)):
        SLV_LoadName = SLV_LoadLog[i].split(' ')
        SLV_LoadName = SLV_LoadName[0]
        SLV_RunPath = (SLV_CMDPath + " " + FilePath + '/' + '/' + SLV_LoadName)
        print(SLV_RunPath)
        os.system(SLV_RunPath)
    print('---VSPAERO is Done---')
    return

#-----------------------------------------------Post 1------------------------------------------------------------#
def Post_1(FilePath, Case, Mode):
    print('---Postprocessing 1---')
    import os
    import glob
    
    NewPath = 'Case' + str(Case) + 'Mode' + str(Mode)
    Post_Path = (FilePath + '/' + NewPath)
    Remove_fem = Post_Path + '\\' + '*.fem'
    Remove_group = Post_Path + '\\' + '*.group.1'
    Remove_adb = Post_Path + '\\' + '*.adb'
    Remove_adb_1 = Post_Path + '\\' + '*.adb.cases'
    [os.remove(f) for f in glob.glob(Remove_fem)]
    [os.remove(f) for f in glob.glob(Remove_group)]
    [os.remove(f) for f in glob.glob(Remove_adb)]
    [os.remove(f) for f in glob.glob(Remove_adb_1)]
    print('---Ending Postprocessing 1---')
    return

#-----------------------------------------------Post 2------------------------------------------------------------#
def Post_2(FilePath, Case, Mode):
    print('---Postprocessing 2---')
    import os
    
    NewPath = 'Case' + str(Case) + 'Mode' + str(Mode)
    Post2_Path = FilePath + '\\' + NewPath
    SLV_LogPath = FilePath + '\\' + 'Log_' + NewPath + '.dat'
    with open(SLV_LogPath, 'r') as file:    
            SLV_LoadLog = file.readlines()
    for i in range(0, len(SLV_LoadLog)):
        Post2_LoadName = SLV_LoadLog[i].split(' ')
        Post2_LoadName = Post2_LoadName[0]
        Post2_OrgPath1 = (FilePath + '/' + Post2_LoadName + '.lod')
        Post2_OrgPath2 = (FilePath + '/' + Post2_LoadName + '.polar')
        Post2_OrgPath3 = (FilePath + '/' + Post2_LoadName + '.history')
        
        lod_ext = "_lod.dat"
        polar_ext = "_polar.dat"
        history_ext = "_hist.dat"
        filename, ext = os.path.splitext(Post2_OrgPath1)
        new_filepath1 = filename + lod_ext
        new_filepath2 = filename + polar_ext
        new_filepath3 = filename + history_ext
        print(new_filepath3)
        if os.path.isfile(os.path.join(Post2_Path, Post2_OrgPath1)):
            os.rename(Post2_OrgPath1, new_filepath1)
        if os.path.isfile(os.path.join(Post2_Path, Post2_OrgPath2)):
            os.rename(Post2_OrgPath2, new_filepath2)
        if os.path.isfile(os.path.join(Post2_Path, Post2_OrgPath3)):
            os.rename(Post2_OrgPath3, new_filepath3)

    print('---Ending Postprocessing 2---')
    return
