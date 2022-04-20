# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 12:51:42 2022

@author: mleong
"""
from Data_Handler.Import_Data import import_data
import pandas as pd
import numpy as np
from datetime import datetime

_AFN_NAME = {"GOLD": "BD Gold",
             "OCEA": "Oceania"
             }
_color = {"GOLD"     : "#97151c",
          "OCEA"     : "#4393c3",
          "PORTFOLIO": "#b5b5b5"} 

_font ={"family":'Raleway',
            "size"  : 10,
            }

#b5b5b5 - default grey
#00788a  
#695955 - black Red   
#00A7BC-oceaniaBlue

# =============================================================================
# Data retrieving modules
# =============================================================================
class retrieve():
    
    def __init__(self,):
        self.last_updated = datetime.now()
        self.ranking = retrieve._ranking()
        self.ts = retrieve._conversion()
        self.percentageDiscount = retrieve._percentageDiscount()
        self.sales = retrieve._sales()
        self.ave = retrieve._ave()
        self.heatmap = retrieve._heatmap()
                               
        self.sales_data_date = self.sales['GOLD'].tail(1).index.droplevel(level="CHANNEL").strftime('%Y-%m-%d')[0]
        self.ctm_data_date   = self.ranking['GOLD'].tail(1).index.strftime('%Y-%m-%d')[0]
        self.Earnix_log_date = self.percentageDiscount.tail(1).index.strftime('%Y-%m-%d')[0]
        
        (self.sales_dict, self.sales_summary,
         self.conversion_dict, self.conversion_summary,
         self.margin_dict)                                   = self._summary()

    @classmethod
    def _ranking(cls):
        '''
        this function pulls ranking data from ctm database
        '''
        #import_cls = import_data('_partner_ranking.sql')
        #df= import_cls.df
        #df.to_csv('_ranking.csv')
        df = pd.read_csv("_ranking.csv", index_col=[0])
        df.loc[:,"DATE"] = pd.to_datetime(df['DATE'])
       
        # filter for AFINITY BRAND
        d={}
        for i in _AFN_NAME:
            d[i] = df.loc[df['AFNTY_BRAND']==i]
    
        for i in d:
           d[i].set_index('DATE', inplace=True)
           d[i] = d[i].drop('AFNTY_BRAND', axis=1)
           d[i].sort_index(inplace=True)
           
        return d
   
    @classmethod
    def _sales(cls):
        '''
        This function pull OCEANIA logs from PCXML and Earnix Log
        '''
        #import_cls = import_data('_sales_volume.sql')
        #df= import_cls.df
        #df.to_csv("_sales_volume.csv")
        df = pd.read_csv("_sales_volume.csv", index_col=[0])
        df.loc[:,"DATE"] = pd.to_datetime(df['DATE'])
        df["VEHICLE_PREMIUM"] =df["VEHICLE_PREMIUM"].astype(float) 

        # filter for AFINITY BRAND
        d={}
        for i in _AFN_NAME:
            d[i] = df.loc[df['AFNTY_BRAND']==i]
            d[i].set_index(['DATE','CHANNEL'], inplace=True)
            d[i] = d[i].drop('AFNTY_BRAND', axis=1)
            d[i].sort_index(inplace=True)
    
        df = pd.concat(d,axis=1).fillna(0)
        
        # make each AFINITY BRAND into a dict
        d={}
        for i in _AFN_NAME:
            d[i]=df[i]
        
        return d

    @classmethod
    def _percentageDiscount(cls):
        '''
        This function pull OCEANIA logs from PCXML and Earnix Log
        '''
        #import_cls = import_data('_percentageDiscount.sql')
        #df= import_cls.df
        #df.to_csv("_percentageDiscount.csv")
        df = pd.read_csv("_percentageDiscount.csv", index_col=[0])
        df.loc[:,"DATE"] = pd.to_datetime(df['DATE'])
        
        df.set_index('DATE', inplace=True)
        df.sort_index(inplace=True)
       
        return df
    
    @classmethod
    def _ave(cls):
        '''
        This function pull the actual vs expected
        '''
        #import_cls = import_data('_AVE.sql')
        #df= import_cls.df
        #df.to_csv("_ave.csv")
        df = pd.read_csv("_ave.csv", index_col=[0])
        df.loc[:,"DATE"] = pd.to_datetime(df['DATE'])
        df.set_index('DATE', inplace=True)
        df.sort_index(inplace=True)
        return df
    
    @classmethod
    def _heatmap(cls):
        '''
        This function make the rank comparison matrix
        '''
        #import_cls = import_data('_rankCompareMatrix.sql')
        #df= import_cls.df
        #df.to_csv("_rankCompareMatrix.csv")
        df = pd.read_csv("_rankCompareMatrix.csv", index_col=[0])
        df.loc[:,"DATE"] = pd.to_datetime(df['DATE'])
        df.set_index('DATE', inplace=True)
        df.sort_index(inplace=True)

        return df
    
    
    @classmethod
    def _conversion(cls):
        '''
        this function aggregate conversion data from ML.conversion
        data includes:
            1. quote count
            2. SOLD count
            3. Margin and premium 
        '''
        #import_cls = import_data('_conversion.sql')
        #df= import_cls.df
        #df.to_csv("_conversion.csv")
        df = pd.read_csv("_conversion.csv", index_col=[0])
        df.loc[:,"DATE"] = pd.to_datetime(df['DATE'])
        
       
        d={} # dataframe for each brand
        c={} # sales and quote count
        pm={} # premium and margin 
        
        # filter for AFINITY BRAND
        for i in _AFN_NAME:
            d[i] = df.loc[df['AFNTY_BRAND']==i]
        
        for i in d:
            # aggregate sales_count and quote_count
            c[i] = d[i].groupby('DATE').agg({'SALES_COUNT':'sum',
                                             'QUOTE_COUNT':'sum'})
            
            # only filter for "SOLD" policy when considering margin and premium 
            pm[i] = d[i].loc[d[i]['SALE_STATUS']=='SOLD'].groupby(
                        'DATE').agg({'MARGIN':'sum',
                                     'VEHICLE_PREMIUM':'sum'})
                                     
      
        c = pd.concat(c,axis=1)
        pm = pd.concat(pm,axis=1)        
                             
        # create multilevel time series
        ts = pd.concat([c,pm], axis=1)
        ts.dropna(subset=[('GOLD','MARGIN')], inplace=True)
  
        return ts
    
    def _summary(self):
       c={} # conversion rate
       m={} # margin
       s={} # sales count
       #q={} # quote count
       for N in [7,14,30,9999]:
           df =self.ts.tail(N).sum()
           c_n = {} #conversion rate for last n period
           s_n = {} #sales count for last n period
           m_n = {} #total margin of last n period
           
           
           # loop through each brand
           for i in _AFN_NAME:    
               m_n[i] = df[i]['MARGIN']
               s_n[i] = df[i]['SALES_COUNT']
               q = df[i]['QUOTE_COUNT']
               c_n[i] = np.divide(s_n[i], q, out=np.zeros_like(s_n[i]), where=q!=0)
       
           # calculate portfolio total
           s_n['PORTFOLIO'] = df["GOLD"]['SALES_COUNT'] + df["OCEA"]['SALES_COUNT'] 
           #q = df["GOLD"]['QUOTE_COUNT']
           #c_n['PORTFOLIO'] = np.divide(s_n['PORTFOLIO'], q, out=np.zeros_like(s_n['PORTFOLIO']), where=q!=0)
           c_n['PORTFOLIO'] = c_n['GOLD'] + c_n['OCEA']
           
           # edit index and column name in each dictionary
           for a,b in [(c,c_n),(s,s_n), (m, m_n)]:
               if N==9999:
                  var = "Since Inception"       #align this with launch date
                  a[var]= pd.DataFrame(b.items())
                  a[var].set_index([0], inplace=True)
                  a[var].rename(columns={1: var}, inplace=True)
               else:
                  a['%sd'%N]= pd.DataFrame(b.items())
                  a['%sd'%N].set_index([0], inplace=True)
                  a['%sd' %N].rename(columns={1: '%sd'%N}, inplace=True)
                     
               
       ## convert dictionary to dataframe
       conv = pd.concat(c, axis=1).applymap(lambda x: "{:.2f}".format( round(x*100, 2) )) 
       conv = conv.astype(str)+'%'   #apply to string
       sale = pd.concat(s, axis=1).applymap(lambda x: "{:,.0f}".format( x))  
       
       # edit names for reporting format
       for frame in [conv,sale]:
           frame.columns = frame.columns.droplevel(level=0)
           frame.rename(index={"GOLD"     : "BD Gold",
                               "OCEA"     : "Oceania",
                               "PORTFOLIO":"Portfolio"}, inplace=True)
       
       # edit format for html used
       def _reassign(df):
           df = df.reset_index().T.reset_index().T
           df.iloc[0,0] = ''
           return df
       conv = _reassign(conv)
       sale = _reassign(sale)
      
       return s,sale, c,conv, m

class update():
    def __init__(self,):
        self.data = retrieve()

data = update()
