import sqlite3
from sqlite3 import Error
from Employee import Employee
from tkinter import *
from tkinter import ttk


def getRows():
    conn = sqlite3.connect('company.db')
    c = conn.cursor()
    with conn:
        c.execute("select * from employees")

    data = c.fetchall()
    print("First Last Pay")
    txt = ""
    for i in data:
        newset = i
        first = i[0]
        last = i[1]
        pay = str(i[2])

        txt += first + " " + last + " " + pay + "\n"
    print(txt)
    return txt


def tableshow(tableName):
    tableShow = Tk()
    conn = sqlite3.connect('company.db')
    lbltext = getRows()
    lblrows = ttk.Label(tableShow, text=lbltext).pack()


def main():
    # initializes the root window
    root = Tk()
    label = ttk.Label(root, text='Choose an Action').pack()
    # gives user an option for what kind of action to perform on the database
    combobox = ttk.Combobox(root)
    combobox.pack()
    combobox.config(values=('insert', 'update', 'delete', 'query'))
    conn = sqlite3.connect('company.db')

    # initializes the GUI for the user to insert their data into the employee table
    def getAction():
        choice = combobox.get()
        if choice == 'insert':
            print('insert')
            insert = Tk()
            lblFirst = ttk.Label(insert, text='enter first name').pack()
            entFirst = ttk.Entry(insert)
            entFirst.pack()
            lbllast = ttk.Label(insert, text='enter last name').pack()
            entLast = ttk.Entry(insert)
            entLast.pack()
            lblpay = ttk.Label(insert, text='enter pay').pack()
            entpay = ttk.Entry(insert)
            entpay.pack()

            def getInsertitems():
                first = entFirst.get()
                last = entLast.get()
                pay = entpay.get()
                emp = Employee(first, last, pay)
                insertemp(emp)
                lableinsert = ttk.Label(insert, text="Row inserted").pack()

            def destroywindow():
                insert.destroy()

            btnInsExc = ttk.Button(insert, text='execute', command=getInsertitems).pack()
            btninsclose = ttk.Button(insert, text="Close", command=destroywindow).pack()

            insert.mainloop()

        if choice == 'delete':
            delete = Tk()
            lbltag = ttk.Label(delete, text="How do you want to delete from the table")
            lbltag.pack()
            com = ttk.Combobox(delete)
            opcom = ttk.Combobox(delete)

            com.pack()
            opcom.pack()
            com.config(values=("First", "Last", "Pay"))
            opcom.config(values=("<", ">", ">=", "=", "like"))
            condition = ttk.Entry(delete)
            condition.pack()

            def getparams():
                comd = com.get()
                ocom = opcom.get()
                cond = condition.get()
                deleteemp(comd, ocom, cond)

            delbtn = ttk.Button(delete, text="delete", command=getparams).pack()
        if choice == 'update':
            update = Tk()
            tableshow("employee")
            lblUpdateChoice = ttk.Label(update, text="Column to update").pack()
            columncombobox = ttk.Combobox(update)
            columncombobox.pack()
            columncombobox.config(values=("First", "Last", "pay"))
            lbl = ttk.Label(update, text="Set the new value below").pack()
            newvalentry = ttk.Entry(update)
            newvalentry.pack()
            lblColchoice = ttk.Label(update, text="which column do you want to base the change on?").pack()
            columncombobox2 = ttk.Combobox(update)
            columncombobox2.pack()
            columncombobox2.config(values=("First", "Last", "pay"))
            operatorcombox = ttk.Combobox(update)
            operatorcombox.pack()
            operatorcombox.config(values=("<", ">", ">=", "=", "like"))
            compentry = ttk.Entry(update)
            compentry.pack()

            def updateParams():
                val1 = columncombobox.get()
                val2 = newvalentry.get()
                val3 = columncombobox2.get()
                val4 = operatorcombox.get()
                val5 = compentry.get()
                updateemp(val1, val2, val3, val4, val5)

            btnupdate = ttk.Button(update, text="Update", command=updateParams).pack()
        if choice == 'query':
            query = Tk()
            lblquery = ttk.Label(query, text="Enter SQL code below").pack()
            querytext = Text(query, width=50, height=20)
            querytext.pack()

            def execquery():
                text = querytext.get("1.0", "end-1c")
                print(text)
                querydatabase(text)

            btnqueryexec = ttk.Button(query, text="Execute", command=execquery).pack()

    button = ttk.Button(root, text='choose', command=getAction).pack()

    c = conn.cursor()

    def insertemp(emp):
        with conn:
            c.execute("insert into employees values(:first, :last, :pay)",
                      {'first': emp.first, 'last': emp.last, 'pay': emp.pay})
            conn.commit()
            tableshow("employees")

    def deleteemp(cond, operator, comp):
        with conn:
            c.execute("delete from employees where " + cond + operator + comp)
            conn.commit()
            tableshow("employees")

    def updateemp(colum, newval, colcondition, operator, condval):
        with conn:

            print(
                "update employees set " + colum + " = '" + newval + "' where " + colcondition + " " + operator + " '" + condval + "'")
            c.execute(
                "update employees set " + colum + " = '" + newval + "' where " + colcondition + " " + operator + " '" + condval + "'")
            conn.commit()
            tableshow("employees")


    def querydatabase(query):
        with conn:
            c.execute(query)
            conn.commit()
            tableshow("employees")

    root.mainloop()


main()
