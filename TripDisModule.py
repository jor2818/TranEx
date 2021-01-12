from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
import csv
import math

#Setting up the Main Frame
root = Tk()
root.title("TRIP DISTRIBUTION MODULE")
width = 500
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2)-(width/2)
y = (screen_height/2)-(height/2)
root.geometry("%dx%d+%d+%d" %(width,height,x,y))
root.resizable(0,0)

#Construct the notebook
main_screen = ttk.Notebook(root)
tab_tripend = ttk.Frame(main_screen)
main_screen.add(tab_tripend, text='1.TRIP END')
tab_travelcost = ttk.Frame(main_screen)
main_screen.add(tab_travelcost,text='2.TRAVEL COST')
tab_analysis = ttk.Frame(main_screen)
main_screen.add(tab_analysis,text = '3.ANALYSIS')
tab_output = ttk.Frame(main_screen)
main_screen.add(tab_output,text='4.OUTPUT')
main_screen.pack(expand=1,fill='both')

def openTE():
    try:
        filename = filedialog.askopenfilename(initialdir="/",filetypes=[("text Document","*.txt"),("All File","*.*")])
        with open(filename) as obj_trip:
            arrayreader = csv.reader(obj_trip)
            global trip_end
            trip_end = []
            trip_end = list(arrayreader)
            #converse header to string
            for i in range(len(trip_end)):
                for j in range(len(trip_end[0])):
                    if i==0:
                        trip_end[i][j]=str(trip_end[i][j])
            #converse number of Zone to integer
            for i in range(1,len(trip_end)):
                trip_end[i][0] = int(trip_end[i][0])
            #converse area to unit of analysis
            for i in range(1,len(trip_end)):
                for j in range(1,len(trip_end[0])):
                        trip_end[i][j] = float(trip_end[i][j])
            #Show the result
            for i in range(1,len(trip_end)):
                tree.insert("",'end',values=(trip_end[i][0],trip_end[i][1],trip_end[i][2]))
        bt1.configure(state='disabled')
        bt2.configure(state='enabled')
    except:
        messagebox.showwarning("Warring....","Error!! input file, Please check the format and value of trip end data")

def openTC():
    try:
        trip_filename = filedialog.askopenfilename(initialdir="/",filetypes=[("text Document","*.txt"),("All File","*.*")])
        with open(trip_filename) as obj_trip:
            arrayreader1 = csv.reader(obj_trip)
            global travelcost
            travelcost = []
            travelcost = list(arrayreader1)
            for i in range(len(travelcost)):
                for j in range(len(travelcost[0])):
                    if i==0 and j==0:
                        travelcost[i][j]=str(travelcost[i][j])
                    else:
                        travelcost[i][j]=int(travelcost[i][j])
        #Show Trip Data
        for i in range(1,len(travelcost)):
            for j in range(1,len(travelcost[0])):
                tree1.insert("",'end',value=(travelcost[i][0],travelcost[0][j],travelcost[i][j]))

        #Check The number of TAZ between Trip end and travel cost data
        if len(trip_end)==len(travelcost):
            bt2.configure(state='disabled')
        else:
            messagebox.showwarning("Warning....","Error!! input file, The number of TAZ between trip end and travel cost data aren't equal!!!")


    except:
        messagebox.showwarning("Warning....","Error!! input file, Please check the format and value of travel cost data")



def selectOD():
    bt4.configure(state='enabled')
    r2_1.configure(state='disabled')
    r2_2.configure(state='disabled')
    ent1.configure(state='disabled')
    ent2.configure(state='disabled')
    ent3.configure(state='disabled')
    bt5.configure(state='disabled')

def selectFun():
    bt4.configure(state='disabled')
    r2_1.configure(state='normal')
    r2_2.configure(state='normal')
    ent1.configure(state='normal')
    ent2.configure(state='normal')
    ent3.configure(state='disabled')
    bt5.configure(state='enabled')

def selectMTL():
    bt4.configure(state='disabled')
    r2_1.configure(state='disabled')
    r2_2.configure(state='disabled')
    ent1.configure(state='disabled')
    ent2.configure(state='disabled')
    ent3.configure(state='normal')
    bt5.configure(state='enabled')

def inputOD():
    try:
        trip_filename = filedialog.askopenfilename(initialdir="/",filetypes=[("text Document","*.txt"),("All File","*.*")])
        with open(trip_filename) as obj_trip:
            arrayreader1 = csv.reader(obj_trip)
            global od_trip
            od_trip= []
            od_trip = list(arrayreader1)
            for i in range(len(od_trip)):
                for j in range(len(od_trip[0])):
                    if i==0 and j==0:
                        od_trip[i][j]=str(od_trip[i][j])
                    else:
                        od_trip[i][j]=int(od_trip[i][j])
        #Show Trip Data
        for i in range(1,len(od_trip)):
            for j in range(1,len(od_trip[0])):
                tree1.insert("",'end',value=(od_trip[i][0],od_trip[0][j],od_trip[i][j]))
        r2.configure(state='disabled')
        r3.configure(state='disabled')
        bt1.configure(state='disabled')
        bt5.configure(state='enabled')
    except:
        messagebox.showwarning("Warning....","Error!! input file, Please check the format and value of origin and destination data")

def opt_bin(travelcost,odsurvey):
    #Find max value on list
    max = 0
    for i in range(1,len(travelcost)):
        for j in range(1,len(travelcost[0])):
            if travelcost[i][j]>max:
                max = travelcost[i][j]
    #set initial interval
    interval = 10
    loop_count = True
    while loop_count:
        b = (max)/interval
        #set bin and sum_bin to zero list
        bin1 = []
        for j in range(interval+1):
            column = []
            for i in range(2):
                column.append(0)
            bin1.append(column)
        sum_bin1 = []
        for j in range(interval+1):
            sum_bin1.append(0)

        for i in range(1,interval+1):
            bin1[i][0] = bin1[i-1][0] + b

        for i in range(1,len(travelcost)):
            for j in range(1,len(travelcost[0])):
                for k in range(1,len(bin1)):
                    if travelcost[i][j]<=bin1[k][0]:
                        sum_bin1[k] = sum_bin1[k] + odsurvey[i][j]
                        break
        
        for i in range(1,len(bin1)):
            bin1[i][1] = sum_bin1[i]

        for i in range(1,len(bin1)):
            if sum_bin1[i]==0:
                break
            else:
                loop_count=False
        interval -= 1

    return bin1

def od_by_survey(tripend,travelcost,otld):
    #Build F(Cij) = 1
    od = []
    for j in range(len(travelcost)):
        column = []
        for i in range(len(travelcost)):
            column.append(1)
        od.append(column)
    
    x = 1
    while x<=10:
        #Set aj,bj,sum_p and sum_a list to zero
        ai = []
        bj = []
        sum_p = []
        sum_a = []
        for i in range(len(travelcost)):
            ai.append(0)
            bj.append(0)
            sum_p.append(0)
            sum_a.append(0)
        #Scale to the production
        for i in range (1,len(travelcost)):
            for j in range(1,len(travelcost)):
                sum_p[i] = sum_p[i]+od[i][j]
        for i in range(1,len(travelcost)):
            ai[i] = tripend[i][1]/sum_p[i]
        for i in range(1,len(travelcost)):
            for j in range(1,len(travelcost)):
                od[i][j]=od[i][j]*ai[i]
        #Scale to the attrction
        for i in range(1,len(travelcost)):
            for j in range(1,len(travelcost)):
                sum_a[j]=sum_a[j]+od[i][j]
        for j in range(1,len(travelcost)):
            bj[j]=tripend[j][2]/sum_a[j]
        for i in range(1,len(travelcost)):
            for j in range(1,len(travelcost)):
                od[i][j]=od[i][j]*bj[j]
        #Build Pridicted trip length distribution
        ptld=[]
        for j in range(len(otld)):
            column = []
            for i in range(len(otld[0])):
                column.append(0)
            ptld.append(column)
    
        for i in range(1,len(otld)):
            ptld[i][0] = otld[i][0]
    
        sum_bin = []
        for j in range(len(otld)):
            sum_bin.append(0)

        #Scale to the distribution function
        for i in range(1,len(travelcost)):
            for j in range(1,len(travelcost[0])):
                for k in range(1,len(ptld)):
                    if travelcost[i][j]<=ptld[k][0]:
                        sum_bin[k] = sum_bin[k] + od[i][j]
                        break
    
        for i in range(1,len(ptld)):
            ptld[i][1] = sum_bin[i]
    
        binfactor = []
        binfactor.append(0)
        for i in range(1,len(ptld)):
            binfactor.append(otld[i][1]/ptld[i][1])

        for i in range(1,len(travelcost)):
            for j in range(1,len(travelcost[0])):
                for k in range(1,len(ptld)):
                    if travelcost[i][j]<=ptld[k][0]:
                        od[i][j] = od[i][j]*binfactor[k]
                        break

        x += 1
    return od

def tripdis_exp(tripend,travelcost,alpha,beta):
    #Calculate the willingness function
    willingness = []
    #Assign the zero to list
    for j in range(len(travelcost)):
        column = []
        for i in range(len(travelcost)):
            column.append(0)
        willingness.append(column)
    #Assign header
    for i in range(len(travelcost)):
        for j in range(len(travelcost[0])):
            if i==0:
                willingness[i][j] = travelcost[i][j]
    for i in range(1,len(travelcost)):
        willingness[i][0] = travelcost[i][0]
    #Assign the willingness
    for i in range(1,len(travelcost)):
        for j in range(1,len(travelcost[0])):
            willingness[i][j] = alpha/math.exp(beta*travelcost[i][j])

    #Loop Banlancing Matrix
    loop_count = True
    while loop_count:
        #Find Banlance Factor ai and bi
        #Set Zero list
        ai = []
        bj = []
        sum_p = []
        sum_a = []
        for i in range(len(travelcost)):
            ai.append(0)
            bj.append(0)
            sum_p.append(0)
            sum_a.append(0)

        for i in range (1,len(travelcost)):
            for j in range(1,len(travelcost)):
                sum_p[i] = sum_p[i]+willingness[i][j]

        for i in range(1,len(travelcost)):
            ai[i] = tripend[i][1]/sum_p[i]

        for i in range(1,len(travelcost)):
            for j in range(1,len(travelcost)):
                willingness[i][j]=willingness[i][j]*ai[i]

        for i in range(1,len(travelcost)):
            for j in range(1,len(travelcost)):
                sum_a[j]=sum_a[j]+willingness[i][j]

        for j in range(1,len(travelcost)):
            bj[j]=tripend[j][2]/sum_a[j]

        for i in range(1,len(travelcost)):
            for j in range(1,len(travelcost)):
                willingness[i][j]=willingness[i][j]*bj[j]

        #Set Total to Zero
        sum_p = []
        sum_a = []
        for i in range(len(travelcost)):
            sum_p.append(0)
            sum_a.append(0)
        for i in range (1,len(travelcost)):
            for j in range(1,len(travelcost)):
                sum_p[i] = sum_p[i]+willingness[i][j]
                sum_a[j]= sum_a[j]+willingness[i][j]
        #Check Error
        er_p = []
        er_a = []
        for i in range(len(travelcost)):
            er_p.append(0)
            er_a.append(0)

        for i in range(1,len(travelcost)):
            er_p[i] = abs(sum_p[i]-tripend[i][1])
            er_a[i] = abs(sum_a[i]-tripend[i][2])

        for i in range(1,len(travelcost)):
            if er_p[i] < 0.1 and er_a[i] < 0.1 :
                loop_count = False
                break
    
    return willingness

def tripdis_power(tripend,travelcost,alpha,beta):
    #Calculate the willingness function
    willingness = []
    #Assign the zero to list
    for j in range(len(travelcost)):
        column = []
        for i in range(len(travelcost)):
            column.append(0)
        willingness.append(column)
    #Assign header
    for i in range(len(travelcost)):
        for j in range(len(travelcost[0])):
            if i==0:
                willingness[i][j] = travelcost[i][j]
    for i in range(1,len(travelcost)):
        willingness[i][0] = travelcost[i][0]
    #Assign the willingness
    for i in range(1,len(travelcost)):
        for j in range(1,len(travelcost[0])):
            willingness[i][j] = alpha/math.pow(travelcost[i][j],beta)

    #Loop Banlancing Matrix
    loop_count = True
    while loop_count:
        #Find Banlance Factor ai and bi
        #Set Zero list
        ai = []
        bj = []
        sum_p = []
        sum_a = []
        for i in range(len(travelcost)):
            ai.append(0)
            bj.append(0)
            sum_p.append(0)
            sum_a.append(0)

        for i in range (1,len(travelcost)):
            for j in range(1,len(travelcost)):
                sum_p[i] = sum_p[i]+willingness[i][j]

        for i in range(1,len(travelcost)):
            ai[i] = tripend[i][1]/sum_p[i]

        for i in range(1,len(travelcost)):
            for j in range(1,len(travelcost)):
                willingness[i][j]=willingness[i][j]*ai[i]

        for i in range(1,len(travelcost)):
            for j in range(1,len(travelcost)):
                sum_a[j]=sum_a[j]+willingness[i][j]

        for j in range(1,len(travelcost)):
            bj[j]=tripend[j][2]/sum_a[j]

        for i in range(1,len(travelcost)):
            for j in range(1,len(travelcost)):
                willingness[i][j]=willingness[i][j]*bj[j]

        #Set Total to Zero
        sum_p = []
        sum_a = []
        for i in range(len(travelcost)):
            sum_p.append(0)
            sum_a.append(0)
        for i in range (1,len(travelcost)):
            for j in range(1,len(travelcost)):
                sum_p[i] = sum_p[i]+willingness[i][j]
                sum_a[j]= sum_a[j]+willingness[i][j]
        #Check Error
        er_p = []
        er_a = []
        for i in range(len(travelcost)):
            er_p.append(0)
            er_a.append(0)

        for i in range(1,len(travelcost)):
            er_p[i] = abs(sum_p[i]-tripend[i][1])
            er_a[i] = abs(sum_a[i]-tripend[i][2])

        for i in range(1,len(travelcost)):
            if er_p[i] < 0.1 and er_a[i] < 0.1 :
                loop_count = False
                break
    
    return willingness

def exportCSV():
    with open('od_volume.csv', 'w', newline='') as csvfile:
        fieldnames = ['From_TAZ', 'To_TAZ','OD_Volume']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(1,len(od)):
            for j in range(1,len(od[0])):
                writer.writerow({'From_TAZ': i, 'To_TAZ': j,'OD_Volume':od[i][j]})

def calOD():
    global od
    if method_var.get() == 1:
        otld = opt_bin(travelcost,od_trip)
        od = od_by_survey(trip_end,travelcost,otld)
        #Show Trip Data
        for i in range(1,len(od)):
            for j in range(1,len(od[0])):
                tree2.insert("",'end',value=(travelcost[i][0],travelcost[0][j],float('{:.0f}'.format(od[i][j]))))
        bt3.configure(state='enabled')
        bt5.configure(state='disabled')
        main_screen.select(3)
    elif method_var.get()==2:
        if function_var.get()==1:
            od = tripdis_power(trip_end,travelcost,alpha_var.get(),beta_var.get())
        else:
            od = tripdis_exp(trip_end,travelcost,alpha_var.get(),beta_var.get())
        #Show Trip Data
        for i in range(1,len(od)):
            for j in range(1,len(od[0])):
                tree2.insert("",'end',value=(travelcost[i][0],travelcost[0][j],float('{:.0f}'.format(od[i][j]))))
        bt3.configure(state='enabled')
        bt5.configure(state='disabled')
        main_screen.select(3)
    else:
        try:
            #od = od_hyman(trip_end,travelcost,mtl_var.get())
            MTL = mtl_var.get()
            beta = []
            beta.append(0)
            beta.append(1/MTL)
            mtl = []
            mtl.append(0)
            od = tripdis_exp(trip_end,travelcost,1,beta[1])
            sum_tc = 0
            sum_t = 0
            for i in range(1,len(travelcost)):
                for j in range(1,len(travelcost)):
                    sum_tc = sum_tc + od[i][j]*travelcost[i][j]
                    sum_t = sum_t + od[i][j]
            
            mtl.append(sum_tc/sum_t)
            #Set next beta
            beta.append(mtl[1]*beta[1]/MTL)
            od = tripdis_exp(trip_end,travelcost,1,beta[2])
            sum_tc = 0
            sum_t = 0
            for i in range(1,len(travelcost)):
                for j in range(1,len(travelcost)):
                    sum_tc = sum_tc + od[i][j]*travelcost[i][j]
                    sum_t = sum_t + od[i][j] 
            mtl.append(sum_tc/sum_t)

            loop_count = True
            a = 3
            while loop_count:
                beta.append((((MTL-mtl[a-2])*beta[a-1]) - ((MTL-mtl[a-1])*beta[a-2])) / (mtl[a-1]-mtl[a-2]))
                od = tripdis_exp(trip_end,travelcost,1,beta[a])
                sum_tc = 0
                sum_t = 0
                for i in range(1,len(travelcost)):
                    for j in range(1,len(travelcost)):
                        sum_tc = sum_tc + od[i][j]*travelcost[i][j]
                        sum_t = sum_t + od[i][j] 
                mtl.append(sum_tc/sum_t)
                if abs(MTL-mtl[a])<=0.001:
                    loop_count = False
                    break
                a = a + 1
            
            lb3.configure(text='F(cij)=1/exp('+str(beta[-1])+'cij)')
            #Show Trip Data
            for i in range(1,len(od)):
                for j in range(1,len(od[0])):
                    tree2.insert("",'end',value=(travelcost[i][0],travelcost[0][j],float('{:.0f}'.format(od[i][j]))))
            bt3.configure(state='enabled')
            bt5.configure(state='disabled')
            main_screen.select(3)
        except:
            messagebox.showwarning("Warning....","Assigned MTL is divergent,Please assign another value!!")
    


#Tab Input Trip End Layout
lb1 = ttk.Label(tab_tripend,text='Input Trip End Data :')
lb1.pack(side=TOP,padx=5,pady=5)
bt1 = ttk.Button(tab_tripend,text='Open file', command=lambda:openTE())
bt1.pack(side=TOP,padx=5,pady=5)
TableMargin = Frame(tab_tripend, width=500)
TableMargin.pack(side=TOP,fill=X,expand=YES,pady=5)
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("TAZ","TP","TA"),height=400,selectmode="extended",yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill = Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill = X)
tree.heading('TAZ',text="TAZ",anchor=W)
tree.heading('TP',text="Trip Production",anchor=W)
tree.heading('TA',text="Trip Attraction",anchor=W)
tree.column('#0',stretch=NO,minwidth=0,width=0)
tree.column('#1',stretch=NO,minwidth=0,width=50)
tree.column('#2',stretch=NO,minwidth=0,width=100)
tree.column('#3',stretch=NO,minwidth=0,width=100)
tree.pack()

#Tab input travel cost data
lb2 = ttk.Label(tab_travelcost,text='Input Travel Cost Data :')
lb2.pack(side=TOP,padx=5,pady=5)
bt2 = ttk.Button(tab_travelcost,text='Open file', command=lambda:openTC())
bt2.pack(side=TOP,padx=5,pady=5)
bt2.configure(state='disabled')
TableMargin1 = Frame(tab_travelcost, width=500)
TableMargin1.pack(side=TOP,fill=X,expand=YES,pady=5)
scrollbarx = Scrollbar(TableMargin1, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin1, orient=VERTICAL)
tree1 = ttk.Treeview(TableMargin1, columns=("From_TAZ","To_TAZ","Cost"),height=400,selectmode="extended",yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree1.yview)
scrollbary.pack(side=RIGHT, fill = Y)
scrollbarx.config(command=tree1.xview)
scrollbarx.pack(side=BOTTOM, fill = X)
tree1.heading('From_TAZ',text="From TAZ",anchor=W)
tree1.heading('To_TAZ',text="To TAZ",anchor=W)
tree1.heading('Cost',text="Travel Cost",anchor=W)
tree1.column('#0',stretch=NO,minwidth=0,width=0)
tree1.column('#1',stretch=NO,minwidth=0,width=100)
tree1.column('#2',stretch=NO,minwidth=0,width=100)
tree1.column('#3',stretch=NO,minwidth=0,width=100)
tree1.pack()

#Tab Analysis Layout
method_var = IntVar()
function_var = IntVar()
alpha_var = DoubleVar()
beta_var = DoubleVar()
mtl_var = DoubleVar()
r1 = tk.Radiobutton(tab_analysis,text='OD Table from Survey',value=1,variable=method_var,command=lambda : selectOD())
r1.pack(anchor=W)
frame1 = ttk.Frame(tab_analysis)
lb4 = ttk.Label(frame1,text='Input OD Survey Data')
lb4.grid(row=0,column=0,sticky=E)
bt4 = ttk.Button(frame1,text='Input OD',command=lambda:inputOD())
bt4.grid(row=0,column=1,sticky=W)
frame1.pack()
r2 = tk.Radiobutton(tab_analysis,text='Distribution or Deterrence Function',value=2,variable=method_var,command=lambda : selectFun())
r2.pack(anchor=W)
frame2 = ttk.Frame(tab_analysis)
Label(frame2,text='Choose function :').grid(row=0,column=0,sticky=W)
r2_1 = tk.Radiobutton(frame2,text='f(Cij)=\u03B1*Cij^(-\u03B2)',value=1,variable=function_var,state='disabled')
r2_1.grid(row=1,column=1,sticky=W)
r2_2 = tk.Radiobutton(frame2,text='f(Cij)=\u03B1*exp(-\u03B2*Cij)',value=2,variable=function_var,state='disabled')
r2_2.grid(row=2,column=1,sticky=W)
function_var.set(1)
Label(frame2,text='Define \u03B1 and \u03B2 value :').grid(row=3,column=0,sticky=W)
lb5 = ttk.Label(frame2,text='\u03B1',width = 5)
lb5.grid(row=4,column=0,sticky=E)
ent1 = ttk.Entry(frame2,textvariable=alpha_var,state='disabled')
ent1.grid(row=4,column=1,sticky=W)
lb6 = ttk.Label(frame2,text='\u03B2',width=5)
lb6.grid(row=5,column=0,sticky=E)
ent2 = ttk.Entry(frame2,textvariable=beta_var,state='disabled')
ent2.grid(row=5,column=1,sticky=W)
alpha_var.set(1.0)
beta_var.set(2.0)
frame2.pack()
r3 = tk.Radiobutton(tab_analysis,text='Mean Trip Length',value=3,variable=method_var,command=lambda : selectMTL())
r3.pack(anchor=W)
frame3 = ttk.Frame(tab_analysis)
lb7 = ttk.Label(frame3,text='MTL')
lb7.grid(row=0,column=0,sticky=W)
ent3 = ttk.Entry(frame3,textvariable=mtl_var,state='disabled')
ent3.grid(row=0,column=1,sticky=W)
method_var.set(1)
frame3.pack()
bt5 = ttk.Button(tab_analysis,text='OD Table',command=lambda:calOD(),state='disabled')
bt5.pack()


#Tab Output Layout
lb3 = ttk.Label(tab_output,text='OD Table')
lb3.pack(side=TOP,padx=5,pady=5)
bt3 = ttk.Button(tab_output,text='Export',command=lambda:exportCSV())
bt3.pack(side=TOP,padx=5,pady=5)
bt3.configure(state='disabled')
TableMargin2 = Frame(tab_output, width=500)
TableMargin2.pack(side=LEFT,fill=X,expand=YES,pady=5)
scrollbarx = Scrollbar(TableMargin2, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin2, orient=VERTICAL)
tree2 = ttk.Treeview(TableMargin2, columns=("From_TAZ","To_TAZ","Trip"),height=400,selectmode="extended",yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree2.yview)
scrollbary.pack(side=RIGHT, fill = Y)
scrollbarx.config(command=tree2.xview)
scrollbarx.pack(side=BOTTOM, fill = X)
tree2.heading('From_TAZ',text="From_TAZ",anchor=W)
tree2.heading('To_TAZ',text="To_TAZ",anchor=W)
tree2.heading('Trip',text="Trip",anchor=W)
tree2.column('#0',stretch=NO,minwidth=0,width=0)
tree2.column('#1',stretch=NO,minwidth=0,width=100)
tree2.column('#2',stretch=NO,minwidth=0,width=100)
tree2.column('#3',stretch=NO,minwidth=0,width=100)
tree2.pack()

#Initializing the Application
if __name__ == '__main__':
    root.mainloop()