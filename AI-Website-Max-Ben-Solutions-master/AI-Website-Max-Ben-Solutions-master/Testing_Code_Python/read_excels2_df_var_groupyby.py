#read excel files out of directory
import glob
in_file = (r"C:\Users\i080272\OneDrive - SAP SE\Documents\oreilly_python_excel\python-powered-excel-master\data\in\*.xlsx")
glob.glob(r"C:\Users\i080272\OneDrive - SAP SE\Documents\oreilly_python_excel\python-powered-excel-master\data\in\*.xlsx")

#check names
for name in glob.glob(in_file):
    print(name)

#simpler way set base path and then searched for extension
import os
files_path = (r"C:\\Users\\i080272\\OneDrive - SAP SE\\Documents\\oreilly_python_excel\\python-powered-excel-master\\data\\in\\")
#files_path = (r"C:\\Users\\i080272\\OneDrive - SAP SE\\Documents\\oreilly_python_excel\\python-powered-excel-master\\data")


in_read_files = glob.glob(os.path.join(files_path,"*.xlsx")) #read in xlsx files

for files in in_read_files: #test
    print(files)

#read into
import pandas as pd

    for file in in_read_files:
        df = pd.read_excel(file)  # has to match glob search excel and xlsx, could be csv etc
        #    print(df)
        #    print(df.dtypes)
        obj_dtypes = df.dtypes.to_dict()
        # make df.dtypes a reg dictionary of strings
        str_dtypes = {}
        for k, v in obj_dtypes.items():
            print(k, v)
            str_dtypes[k] = str(v)
        str_dtypes
        # group by can be a list of columns but we only want object
        groupby_var = []
        # aggregates can be dictionary
        agg_var = {}

        for k, v in str_dtypes.items():
            if v == 'object':
                groupby_var.append(k)
            elif v == 'int64':
                agg_var[k] = 'sum'
            elif v == 'float64':
                agg_var[k] = 'sum'
        print("groupby_var...", groupby_var)
        print('agg_var.....', agg_var)

        # now we have a list of groupby variables and agg_vars
        # we will keep agg_var the same
        # we need to vary the columns

    print("columns are:", len(groupby_var))
    #how many permutations of the columns?
    #for example if [1,2] then [1],[2], [1,2], [2,1] for [1,2,3,4,5] then many more

    import itertools
    p_len = len(groupby_var)
    p = list(itertools.permutations(groupby_var, 1))
    print('perms are:', p )
    p = list(itertools.permutations(groupby_var, 2))
    print('perms are:', p )

#
    count = 0
    perm_list = []
    perms = len(groupby_var) + 1

    for x in range(perms):
        # print(x)
        p = list(itertools.permutations(groupby_var, x))
        p_len = len(p)
        print(p_len)
        count = count + p_len
        perm_list.append(p)
        print(perm_list)
    print(count - 1)

    #first item is the empty set [[()]] just delete it...
    del perm_list[0]

    print("Parameters so far:")
    print('grouby_var :', groupby_var)
    print('agg_var    :', agg_var)
    print("Colum perms:", perm_list)

    #list of type tuple, go through each list convert to list type
    #display first 3 rows

    #make file names rather than sheets for now

    for r in range(len(perm_list)):
        for n in range(len(perm_list[r])):
#            print(perm_list[r][n])
            g_var = list(perm_list[r][n])
            print('Column list:', g_var)
            print(df.groupby(g_var).agg( agg_var ).iloc[:3])
            df_grouped = df.groupby(g_var).agg( agg_var )  #this gets written out to file
            ct = (list(perm_list[r][n]))
#            print("File names:",ct)
            label = "_".join(ct)
            print("File name would be: ", label)
            output_file = os.path.join( files_path, 'sales'+label+'.xlsx') #<===== hard coded file name...
            print("out ", output_file)
            df_grouped.to_excel(output_file)
            print("done!")




