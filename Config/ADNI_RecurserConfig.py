__author__ = 'wang'

fileExtensionDict = {'dcm': 'dicom',
                     'dcm.gz': 'dicom',
                     'nii': 'nifti',
                     'nii.gz': 'nifti',
                     'mnc': 'minc',
                     'mnc.gz': 'minc',
                     'v': 'v'}

fileExtensionTuple = ('.nii', '.dcm', '.mnc', '.nii.gz', '.dcm.gz', '.mnc.gz', '.v', '.v.gz')

scanTypeDict = {
                '4x5minute_frames_4i_16s__AV45': 'AV45',
                '4x5minute_frames_-_Iter_Bra_AV45': 'AV45',
                '50-70_min_dynamic-3D_4i_16s_AV45': 'AV45',
                'ADNI2_AV45__AC_': 'AV45',
                'ADNI_BRAIN_3D__AV45': 'AV45',
                'ADNI_Brain_PET__Raw_AV45': 'AV45',
                'ADNIGO_-_AV45_BRAIN_STUDY': 'AV45',
                'ADNI_GO_PRIMARY__AV45': 'AV45',
                'ASL_PERFUSION': 'ASL_P',
                'AV45_Dyn_4x5min_2Di_336_2z_AllPass__AC_': 'AV45',
                'Average_DC': 'Ave_DC',
                'Axial_DTI': 'A_DTI',
                'Dyn_ADNI-GO_128x,4i20s,256mmFOV,NoFilter___AV45': 'AV45',
                'Enhanced_Axial_DTI': 'EA_DTI',
                'Extended_Resting_State_fMRI': 'ext-rsfmri',
                'Fractional_Aniso.': 'F_Aniso',
                'Fractional_Ansio.': 'F_Aniso',
                'Isotropic_image': 'I_image',
                'MoCoSeries': 'MoCo',
                'MPR__GradWarp': 'MPR',
                'MPR__GradWarp__Mask': 'MPR_M',
                'MPR__GradWarp__N3': 'MPR_N3',
                'MPR__GradWarp__B1_Correction': 'MPR_B1',
                'MPR__GradWarp__B1_Correction__N3': 'MPR_B1_N3',
                'MPR__GradWarp__B1_Correction__N3__Scaled': 'MPR_B1_N3S',
                'MPR__GradWarp__B1_Correction__N3__Scaled_2': 'MPR_B1_N3S',
                'MPR-R__GradWarp__B1_Correction__N3': 'MPR-R_B1_N3',
                'MPR__GradWarp__B1_Correction__Mask': 'MPR_B1_M',
                'MPR-R__GradWarp': 'MPR-R',
                'MPR-R__GradWarp__Mask': 'MPR-R_M',
                'MPR-R__GradWarp__N3': 'MPR-R_N3',
                'MPR__GradWarp__N3__Scaled': 'MPR_N3S',
                'MPR-R__GradWarp__N3__Scaled': 'MPR-R_N3S',
                'MPR-R__GradWarp__N3__Scaled_2': 'MPR-R_N3S',
                'MPR-R__GradWarp__B1_Correction': 'MPR-R_B1',
                'MPR-R__GradWarp__B1_Correction__Mask': 'MPR-R_B1_M',
                'MPR-R__GradWarp__B1_Correction__N3__Scaled': 'MPR-R_B1_N3S',
                'MPR-R__GradWarp__B1_Correction__N3__Scaled_2': 'MPR-R_B1_N3S',
                'MT1__GradWarp__N3m': 'MT1_G_N3m',
                'MT1__N3m': 'MT1_N3m',
                'Perfusion_Weighted': 'Perf_W',
                'PET_AC_3D_BRAIN__AV45': 'AV45',
                'PET_Brain_AV_45__AV45': 'AV45',
                'PET_Brain_COR_ADNI_#2__AC__AV45': 'AV45',
                'relCBF': 'relCBF',
                'Spatially_Normalized,_Masked_and_N3_corrected_T1_image': 'T1-SNMN3C',
                'PET_Brain__AV45': 'AV45',
                '3D_ADNI2_AV45_F18_ACQUI._4i_16s': 'AV45',
                'ADNI2_FDG__AC_': 'FDG',
                '30_min_3D_FDG_4i_16s': 'FDG',
                '[F-18]_20_min_4i_16s__AV45': 'AV45',
                'Resting_State_fMRI': 'rsfmri',
                'HHP_6_DOF_AC-PC_registered_MPRAGE': 'HHP6MPRAGE',
                'EPI_corrected_image': 'EPIC_DTI',
                'EPI_current_corrected_image': 'EPI_DTI',
                'corrected_AD_image': 'Corr_ADDTI',
                'Axial_T2-FLAIR': 'A_T2_FL',
                'ADNIGO_-_FDG_BRAIN_STUDY': 'FDG',
                'ASL_PERFUSION_EYES_OPEN_': 'ASL_PERF_EO',
                'ASL_PERFUSION_EYE_OPEN': 'ASL_PERF_EO',
                'MPR-R____N3': 'MPR-R__N3',
                'MPR____N3__Scaled_2': 'MPR__N3S',
                'MPR____N3__Scaled': 'MPR__N3S',
                'MPR____N3': 'MPR__N3',
                'MPR__GradWarp__N3__Scaled_2': 'MPR_N3S',
                'Axial_FLAIR': 'A_FL',
                'Sag_IR-SPGR': 'S_IR-SPGR',
                'Accelerated_Sag_IR-SPGR': 'AS_IR-SPGR',
                'Accelerated_Sag_IR-FSPGR': 'AS_IR-FSPGR',
                'Sag_IR-FSPGR': 'S_IR-FSPGR',
                'Accelerated_SAG_IR-SPGR': 'AS_IR-SPGR',
                'Accelerated_SAG_IR-FSPGR': 'AS_IR-SPGR',
                'AX_T2_FLAIR': 'A_T2_FL',
                'AX_T2_FLAIR_NO_ANGLE': 'A_T2_FL_NA',
                'Axial_T2-FLAIR_repeat': 'A_T2_FL_Rep',
                'IR-FSPGR': 'IR-FSPGR',
                'IR-FSPGR-Repeat': 'IR-FSPGR_Rep',
                'MPR____Mask': 'MPR__M',
                'MPR-R____Mask': 'MPR-R__M',
                'AX_FLAIR': 'A_FL',
                'Axial_DTI_HEAD_24_': 'A_DTI_H24',
                'corrected_MD_image': 'DTI_C_MD',
                'Eddy_current_corrected_image': 'DTI_ECC',
                'corrected_RD_image': 'DTI_C_RD',
                'corrected_FA_image': 'DTI_C_FA',
                'Axial_rsfMRI__Eyes_Open_': 'A_rsfmri_EO',
                'ASL_PERF': 'ASL_PERF',
                'Average_DC_-PJ': 'Ave_DC_PJ',
                'Axial_DTI__-PJ': 'A_DTI_PJ',
                'Spatially_Normalized,_Masked_and_N3_corrected_T2_image': 'T2-SNMN3C',
                'Extended_Resting_State_fMRI_CLEAR': 'ext-rsfmri',
                'epi_2s_resting_state': 'rsfmri',
                }
