# -*- coding: utf-8 -*-
'''
% This file extracts features from input dataframe of a specific patient
% the output is a dataframe with the extracted features
% 
% /**************************************************************************** 
%  * Job:             Feature Extraction                                      * 
%  * Description: This script generates  extracted features
%           it generates 44 features for each window for each electrode
%                                     * 
%  *Inputs: signal dataframe from preparation steps
%  *                                                                          * 
%  * Generated on:    Sun, May 14, 2017                                       * 
%  * Generated by:    Gamal Elkomy                                            * 
%  * Version:         1                                                       * 
%  ****************************************************************************/ 
'''

import pandas as pd
from scipy.signal import welch
import datetime
from calculate_features import calculate_features


#data= pd.read_csv(r'C:\Users\Gamal\Downloads\samples - Copy.csv')
#data["'Time and date'"]= pd.to_datetime(data["'Time and date'"], format="%H:%M:%S.%f %d/%m/%Y")
#data.index= data["'Time and date'"]
#del data["'Time and date'"]
#data= preprocessing(r'E:\Faculty of Engineering\InnoTech\Python Release')

def feature_extraction(data):
    first=min(data.index)
    period=max(data.index)-first-datetime.timedelta(seconds=4)
    all_windows={}
    window_list= [first + datetime.timedelta(seconds=x) for x in range(0, int(period.seconds+round(float(period.microseconds)/1000000))+1,2)]
    
    for window_start in window_list:
        window_end=window_start+datetime.timedelta(seconds=4)
        window_data=data.loc[window_start: window_end]
        Fxx, Pxx = welch(x=window_data, fs=256, nperseg=256, noverlap=2,axis=0)
        Pxx=pd.DataFrame(Pxx,columns=window_data.columns)
        temp=calculate_features(Pxx)
        if len(all_windows)==0:
            all_windows={k:pd.DataFrame(v).T for k,v in temp.iteritems()}
        else:
            for k in temp.iterkeys():
                items=pd.DataFrame(data=temp[k]).T
                all_windows[k]= pd.concat([items, all_windows[k]], axis=0)
    return all_windows
