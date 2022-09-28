import os
import datetime
import win32com.client

PURGE_EXECUTED= False
bcutil_path= r"NYI" # Path to BreakConns XLAM file
saved_files= []

def genrep(fn):
    xlx= win32com.client.DispatchEx("excel.application")
    xlx.Visible= True
    wbx= xlx.Workbooks.Open(fn)
    for cnx in wbx.Connections:
        print("Refreshing: '{}'".format(cnx.Name))
        cnx.Refresh()
        print("Refresh complete")
    
    print("Severing connections...")
    wbx.Activate()
    xlx.Workbooks.Open(bcutil_path)
    r=True
    while r:
        i=0
        for k in xlx.Workbooks:
            try:
                i+= 1 if 'breakconns' in k.Name else 0
            except:
                pass
        r= bool(i)
    print("Connections have been murdered")
    
    print("Cleaning up mess...")
    wsx = wbx.Worksheets(1)
    wsx.Range("A1").Formula = wsx.Range("A1").Value
    try:
        xlx.DisplayAlerts= False
        wbx.Worksheets('meta').Delete()
        xlx.DisplayAlerts= True
    except:
        xlx.DisplayAlerts= True
    print("Consumable prepped for extract")
    
    print("Isolating to client...")
    t= wbx.Path
    tstart= len(p)+1
    acct= t[tstart:]
    basename= wbx.Name[:-5] #remove .xlsx
    datestamp= str(datetime.date.today())
    outputname= basename + ' ' + datestamp
    outputpath= rp + '\\' + "products" + '\\' + acct + '\\' + outputname + ".xlsx"
    wbx.SaveAs(outputpath)
    print("File saved: {}".format(outputpath))
    saved_files.append(outputpath)
    print("Terminating session\n\n")
    xlx.Quit()

def exitloop():
    if len(errs) > 0:
        z= input('Would you like to retry errors? Y/N  : ')[0].upper()
        if z=='Y':
            print("Retrying errors.\n")
            for i in errs:
                print('Path {}'.format(i))
                try:
                    genrep(i)
                except:
                    print("THIS FILE HAS FAILED: MANUAL RESOLUTION REQUIRED")
        elif z=='N':
            print("okie dokie. buhbye.")
        elif z=='M':
            print("Manual resolution path entered. Once preprocessing remedy applied, please enter file path to process.")
            Q= "Let's Go"
            while len(Q)>0:
                Q= ""
                Q= input("File Path:\n")
                if len(Q)>0:
                    genrep(Q)
                else:
                    pass # in case something else strikes me in the head
        elif z=='P': # Delete everything created in saved_files
            global PURGE_EXECUTED
            if not(PURGE_EXECUTED):
                print("BEGIN THE PURGE!")
                for i in saved_files:
                    try:
                        os.remove(i)
                    except:
                        print("Whoa, {} has some bigger issues.".format(i))
            else:
                print("Cannot purge more than once in the same runtime.")
        else:
            pass  # because reasons
    else:
        z= "N" # There were no errors, so the retry options will not print. No manual resolution option. Will need future refactor.
    return z

# ---
if __name__=="__main__":
    print('\n')
    
    rp= r'NYI' #PATH to Reports Directory
    p= rp + '\\' + 'machines'
    pk= [p + '\\' + i for i in os.listdir(p) if os.path.isdir(p + '\\' + i)]
    fns= [dr + '\\' + i for dr in pk for i in os.listdir(dr) if i[-5:] == '.xlsx']
    
    errs= []
    for fn in fns:
        print('Path {}'.format(fn))
        try:
            genrep(fn)
        except:
            errs.append(fn)
            print('This file failed. Moving to next. \n\n')
    
    z= "X"
    while len(z)>0:
        z= exitloop()
        if z=="N":
            z=""
        elif z=="P":
            PURGE_EXECUTED= True

