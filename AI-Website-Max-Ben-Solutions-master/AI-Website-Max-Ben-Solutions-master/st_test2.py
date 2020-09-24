import streamlit as st
import pandas as pd
import pydeck as pdk

#df = pd.read_excel('sales.xlsx')

st.write("## dont run with more than 4 columns! it does permutations!")

age = st.slider('How old are you?', 0, 130, 25)


uploaded_file = st.file_uploader("Choose a Excel file", type="xlsx")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write(df)
    obj_dtypes = df.dtypes.to_dict()
    print(obj_dtypes)
    # make df.dtypes a reg dictionary of strings
    str_dtypes = {}
else:
    st.write("wtf")

options = st.multiselect('What are your favorite colors', ['Green', 'Yellow', 'Red', 'Blue'], ['Yellow', 'Red'])
st.write('You selected:', options)


for k, v in obj_dtypes.items():
#   st.write(k, v)
    str_dtypes[k] = str(v)
    #str_dtypes
    # group by can be a list of columns but we only want object
    groupby_var = []
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

option = st.selectbox(
    'How would you like to group the data?',
    (groupby_var))
st.write('You selected:', option)

option = st.selectbox(
    'How would you like to group the data?',
    ('Worker','Month','Client', 'Qty'))
st.write('You selected:', option)


import itertools
p_len = len(groupby_var)
p = list(itertools.permutations(groupby_var, 1))
#st.write('perms are:', p )
p = list(itertools.permutations(groupby_var, 2))
#st.write('perms are:', p )


count = 0
perm_list = []
perms = len(groupby_var) + 1


for x in range(perms):
    # st.write(x)
    p = list(itertools.permutations(groupby_var, x))
    p_len = len(p)
#   st.write(p_len)
    count = count + p_len
    perm_list.append(p)
#   st.write(perm_list)
#st.write(count - 1)

#first item is the empty set [[()]] just delete it...
del perm_list[0]

#list of type tuple, go through each list convert to list type
#display first 3 rows

#make file names rather than sheets for now

for r in range(len(perm_list)):
    for n in range(len(perm_list[r])):
#            st.write(perm_list[r][n])
        g_var = list(perm_list[r][n])
#        st.write('Column list:', g_var)
        st.write(df.groupby(g_var).agg( agg_var ).iloc[:5])
        df_grouped = df.groupby(g_var).agg( agg_var )  #this gets written out to file
        ct = (list(perm_list[r][n]))
#            st.write("File names:",ct)
        label = "_".join(ct)
        st.write("File name would be: ", label)
        # output_file = os.path.join( files_path, 'sales'+label+'.xlsx') #<===== hard coded file name...
        # st.write("out ", output_file)
        # df_grouped.to_excel(output_file)
#        st.write("done!")
