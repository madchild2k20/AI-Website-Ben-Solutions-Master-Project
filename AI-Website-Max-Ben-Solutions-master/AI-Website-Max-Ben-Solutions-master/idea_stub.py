############# stub program for idea
#get a file, show user columns
#let user pick columns for group by
#############
import pandas as pd

#all files have to be in same directory testing with sales ...
file = input('Input file, leave blank for  sales.xlsx: ')
#if blank go with sales.xlsx
if file =='':
    file = 'sales.xlsx'

df = pd.read_excel(file)

df_cols = df.columns.to_list()
print("Columns are :", df_cols)

#let user pick which columns
prompt = str(df_cols) + " pick for group by "
df_cols_selected = input(prompt)
print("You picked ... "+df_cols_selected)
df_cols_selected_list = df_cols_selected.split()
print("Converts into list : ", df_cols_selected_list)


obj_dtypes = df.dtypes.to_dict()
# make df.dtypes a reg dictionary of strings
str_dtypes = {}
for k, v in obj_dtypes.items():
    print(k, v)
    str_dtypes[k] = str(v)
str_dtypes
# group by can be a list of columns but we only want object
groupby_var = df_cols_selected_list
# aggregates can be dictionary
agg_var = {}
#aggvalues =['sum','mean','std','count','nth','custom ']
for k, v in str_dtypes.items():
    if v == 'object':
        groupby_var.append(k)
    elif v == 'int64':
        agg_var[k] = 'sum'
    elif v == 'float64':
        agg_var[k] = 'sum'
print("groupby_var...", groupby_var)
print('agg_var.....', agg_var)


print(df.groupby(df_cols_selected_list).agg( agg_var ).iloc[:10])
df_grouped = df.groupby(df_cols_selected_list).agg( agg_var )  #this gets written out to file

#writing a file out with groupby indicated at the end
#split at dot add underscore
file_prefix = file.rsplit('.', 1)[0]+'_'

#remove space from columns list
df_cols_selected = df_cols_selected.rstrip(' ')
#add underscore
file_suffix = df_cols_selected.replace(' ','_')
grouped_file_name = file_prefix + file_suffix
print("Grouped by file :", grouped_file_name)

#writing file out using pd
df_grouped.to_excel(grouped_file_name+'.xlsx', engine='xlsxwriter')


