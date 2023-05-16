import mysql.connector
import datetime
from tabulate import tabulate
con=mysql.connector.connect(host="localhost",
                            user="root",
                            password="87654321",
                            database="practice")
cur=con.cursor()

def menu():
    print('~'*120)
    print(" "*49+"Hotel THE PARADISE INN",'~'*120,sep=('\n'))
    print(" "*46+"GREETINGS! HOW CAN I HELP YOU?\n\n")
    print(" "*35+"1. ROOMS:\n\n"," "*43+"a. NEW BOOKING\n"," "*43+"b. VIEW ROOM LIST\n"," "*43+"c. FIND A VACANT ROOM\n"," "*43+"d. EDIT GUEST DETAILS\n")
    print(" "*35+"2. RESTAURANT:\n\n"," "*43+"a. VIEW MENU\n"," "*43+"b. GENERATE BILL\n")
    print(" "*35+"3. PAYMENT\n")
    print(" "*35+"4. EXIT\n")
    opt=int(input(" "*34+">>> ENTER YOUR CHOICE: "))
    if opt==1:
        rooms()
    elif opt==2:
        restaurant()
    elif opt==3:
        bill()
    elif opt==4:
        pass


    
def rooms():
    print('')
    print('~'*120)
    print(" "*49+"MANAGE ROOMS",'~'*120,sep=('\n'))
    print("")
    print(" "*36+"1). NEW BOOKING\n\n"," "*35+"2). VIEW ROOM LIST\n\n"," "*35+"3). VACANT ROOMS\n\n"," "*35+"4). EDIT GUEST DETAILS\n\n"," "*35+"5). EXIT\n")
    chR=int(input(" "*34+">>> ENTER YOUR CHOICE: "))
    if chR==1:
        form()
        rooms()
    elif chR==2:
        print("\n  HERE IS A LIST OF ALL THE ROOMS")
        print('')
        cur.execute("Select * from ROOMS")
        data=cur.fetchall()
        h1=['ROOM NO','NAME','PHONE NO','ADDRESS','CHECK-IN','CHECK-OUT','TYPE','FOOD PREF']
        print(tabulate(data,headers=h1,tablefmt='psql'))
        rooms()
    elif chR==3:
        print("\n  HERE IS A LIST OF VACANT ROOMS:")
        print('')
        cur.execute("Select ROOM_NO,R_PREF from ROOMS where CHECK_IN IS NULL")
        data=cur.fetchall()
        h1=['ROOM NO','TYPE']
        print(tabulate(data,headers=h1,tablefmt='psql'))
        rooms()
    elif chR==4:
        guest()
    elif chR==5:
        menu()


def form():
    print('')
    print(" "*30+'='*50)
    print(" "*42+"PLEASE FILL IN THE DETAILS"," "*30+'='*50,sep=('\n'))
    print("")
    cur.execute("Select ROOM_NO,R_PREF from ROOMS where CHECK_IN IS NULL")
    data=cur.fetchall()
    h1=['ROOM NO','TYPE']
    print("List of available rooms")
    print(tabulate(data,headers=h1,tablefmt='psql'))
    vac=int(input(" "*36+"ENTER ROOM NUMBER: "))
    if vac==0:
        rooms()
    vrn=[101,102,103,104,105,106,107,108,109,110]
    lisrn=[]
    r=0
    for i in data:
        j=list(i)
        lisrn.append(data[len(lisrn)][0])    
    if vac in vrn:
        if vac in lisrn:
            name=input(" "*36+"Full Name: ")
            adr=input(" "*36+"Address: ")
            i=0
            while True:
                phno=int(input(" "*36+"Phone number: +91 "))
                if len(str(phno))>10:
                    print('\n'," "*35+"Way too long... Try again (Enter 10 digit number)")
                elif len(str(phno))<10:
                    print('\n'," "*35+"Way too short... Try again (Enter 10 digit number)")    
                else:
                    break
            print(" "*36+"Check-In date:")
            c_in=dates()
            stday=c_in-datetime.date.today()
            stay=stday.days
            while stay<=0:
                print('\n'," "*35+"Can't take this date! Please enter a valid date")
                c_in=dates()
                stday=c_in-datetime.date.today()
                stay=stday.days

            cur.execute("UPDATE ROOMS SET NAME='%s',PHONE_NO=%s,ADDRESS='%s',CHECK_IN='%s' WHERE ROOM_No=%s"%(name,phno,adr,c_in,vac))
            con.commit()
            print("\n"," "*36+"ROOM HAS BEEN BOOKED!")
        else:
            print(" "*36+"ROOM IS PRE-OCCUPIED !!!")
            form()
    else:
        print(" "*36+"INCORRECT ROOM NUMBER ENTERED")
        form()
    rooms()

def guest():
    print('')
    print(" "*30+'='*50)
    print(" "*38+"CHOOSE THE DETAIL YOU WANT TO EDIT"," "*30+'='*50,sep=('\n'))
    print("")
    print(" "*36+"1). NAME\n\n"," "*35+"2). PHONE NUMBER\n\n"," "*35+"3). ADDRESS\n\n"," "*35+"4). CHECK_OUT DATE\n\n"," "*35+"5). EXIT\n")
    ch=int(input(" "*36+">>>  WHAT DO YOU WANT TO EDIT: "))
    if ch==1:
        ro_no=int(input(" "*36+">>>  ENTER ROOM NUMBER OF THE GUEST: "))
        name=input(" "*36+">>>  ENTER THE NEW NAME: ")
        cur.execute("UPDATE ROOMS SET NAME='%s' WHERE ROOM_NO=%s"%(name,ro_no))
        con.commit()
        print("")
        print(" "*36+"NAME HAS BEEN SUCCESSFULLY UPDATED !!")
        guest()
    elif ch==2:
        ro_no=int(input(" "*36+">>>  Enter Room number of the Guest: "))
        phno=int(input(" "*36+">>>  Enter new Phone number: +91 "))
        if len(str(phno))>10:
            print('\n'," "*36+"Way too long... Try again (Limit 10 digits)")
            guest()
        else:
            cur.execute("UPDATE ROOMS set PHONE_NO=%s where ROOM_NO=%s"%(phno,ro_no))
            con.commit()
            print('\n'," "*36+"PHONE NUMBER HAS BEEN SUCCESSFULLY UPDATED !!")
            guest()
    elif ch==3:
        ro_no=int(input(" "*36+">>>  Enter Room number of the Guest: "))
        adr=input(" "*36+">>>  Enter new Address: ")
        cur.execute("UPDATE ROOMS set ADDRESS='%s' where ROOM_NO=%s"%(adr,ro_no))
        con.commit()
        print(" "*36+"ADDRESS HAS BEEN SUCCESSFULLY UPDATED !!")
        guest()
    elif ch==4:
        ro_no=int(input(" "*36+">>>  Enter Room number of the Guest: "))
        print(" "*36+">>>  Check_Out date: ")
        chkout=dates()
        cur.execute("UPDATE ROOMS set CHECK_OUT='%s' where ROOM_NO=%s"%(chkout,ro_no))
        con.commit()
        print(" "*36+"CHECK_OUT DATE HAS BEEN SUCCESSFULLY UPDATED !!!")
        guest()
    elif ch==5:
        rooms()


def restaurant():
    print('')
    print('~'*120)
    print(" "*49+"REATAURANT",'~'*120,sep=('\n'))
    print("")
    print(" "*36+"1). VIEW MENU\n\n"," "*35+"2). GENERATE BILL\n\n"," "*35+"3). EXIT\n")
    opt2=int(input(" "*36+">>>  Enter your choice: "))
    if opt2==1:
        print('')
        print('~'*34)
        print("             MENU")
        print('~'*34,'\n')
        cur.execute("SELECT * FROM MENU")
        data=cur.fetchall()
        h1=['ITEM NO','ITEM','PRICE','TYPE']
        print(tabulate(data,headers=h1,tablefmt='psql'))
        restaurant()
    elif opt2==2:
        generate()
    elif opt2==3:
        menu()


def generate():
    rno=int(input(" "*36+">>>  Enter the room number: "))
    conf='y'
    lis=[]
    
    while conf=='y':
        ord=int(input(" "*36+">>>  Enter the ITEM NUMBER of the dish: "))
        lis.append(ord)
        conf=input(" "*36+">>>  Enter another one? (y/n): ")

    print(" "*36,'='*34,'\n\n'," THE ITEMS ORDERED ARE:",'\n')
    for j in lis:
        cur.execute("insert into ordered values(%s,%s)"%(rno,j))
        con.commit()
        
    cur.execute("SELECT O.ITEM_NO ITEM_NO ,M.ITEM NAME ,M.PRICE COST FROM ORDERED O natural join MENU M where O.ROOM_NO=%s"%(rno))
    data=cur.fetchall()
    h1=['ITEM NO','ITEM','PRICE']
    print(tabulate(data,headers=h1,tablefmt='psql'))

    cur.execute("SELECT SUM(M.PRICE) FROM MENU M natural join ORDERED O where O.ROOM_NO=%s"%(rno))
    data=cur.fetchall()
    res_bill=data[0][0]
    print(" "*36+">>>  TOTAL AMOUNT TO BE PAID: ",res_bill)
    print(" "*36+"AMOUNT HAS BEEN ADDED TO THE FINAL BILL !")
    restaurant()

    
def bill():
    print('')
    print('~'*120)
    print(" "*49+"BILL",'~'*120,sep=('\n'))
    print("")
    rout=int(input(" "*27+">>>  ENTER THE ROOM NUMBER TO PROCEED TO CHECK-OUT: "))
    
    cur.execute("SELECT CHECK_IN FROM ROOMS WHERE ROOM_NO=%s"%(rout))
    data=cur.fetchall()
    ch_in=data[0][0]
    if ch_in is None:
        print(" "*42+"THIS ROOM IS VACANT !!!")
        bill()
        
    ch_out=datetime.date.today()
    diff=ch_out-ch_in
    
    cur.execute("select name from rooms where room_no=%s"%(rout))
    data=cur.fetchone()
    print('\n'," "*35+"NAME OF THE GUEST: ",data[0])
    
    cur.execute("select CHECK_IN from rooms where room_no=%s"%(rout))
    data=cur.fetchone()
    
    print(" "*36+"CHECK-IN DATE: ",ch_in)
    print(" "*36+"CHECK-OUT DATE: ",ch_out)
    print(" "*36+"TOTAL NUMBER OF DAYS: ",diff.days)
    
    cur.execute("select r_pref from rooms where room_no=%s"%(rout))
    data=cur.fetchone()
    print(" "*36+"TYPE OF ROOM: ",data[0])
    if data[0] in "STANDARD" or "standard":
        print(" "*36+"PRICE FOR ONE DAY FOR STANDARD ROOMS: 1000")
        room=diff.days*1000

    elif data[0] in "DELUXE" or "deluxe":
        print('')
        print(" "*36+"PRICE FOR ONE DAY FOR DELUXE ROOMS: 1500")
        room=diff.days*1500

    elif data[0] in "SUITE" or "suite":
        print('')
        print(" "*36+"PRICE FOR ONE DAY FOR SUITE ROOMS: 2500")
        room=diff.days*2500

    cur.execute("SELECT SUM(M.PRICE) FROM MENU M natural join ORDERED O where O.ROOM_NO=%s"%(rout))
    data=cur.fetchall()
    res_bill=data[0][0]
    cur.execute("select count(*) from ordered where room_no=%s"%(rout))
    data=cur.fetchall()
    if data[0][0]==0:
        print(" "*36+"RESTAURANT BILL: ", res_bill)
        print(" "*36+"TOTAL AMOUNT PAYABLE : ",room)
    else:
        print(" "*36+"Restaurant bill: ", res_bill)
        print(" "*36+"TOTAL AMOUNT PAYABLE : ",room+res_bill)
    
    payment()
    
    print('')
    print(" "*36+'~'*34)
    print(" "*41+"THANK YOU VISIT AGAIN :)")
    print(" "*36+'~'*34,)
    cur.execute("DELETE FROM ORDERED WHERE ROOM_NO=%s"%(rout))
    con.commit()
    cur.execute("UPDATE ROOMS SET NAME=NULL,PHONE_NO=NULL,ADDRESS=NULL,CHECK_IN=NULL,CHECK_OUT=NULL, F_PREF=NULL WHERE ROOM_NO=%s"%(rout))
    con.commit()
    menu()

    
def payment():
    print(" "*36+"CHOOSE MODE OF PAYMENT\n\n"," "*35+"1). CREDIT CARD\n\n"," "*35+"2). DEBIT CARD\n\n"," "*35+"3). CASH\n")
    paymeth=int(input(" "*36+">>>  CHOICE:"))
    confrm=input(" "*36+">>>  AMOUNT PAID(y/n): ")


def dates():
    Y=int(input(" "*40+"Enter Year: "))
    M=int(input(" "*40+"Enter Month: "))
    D=int(input(" "*40+"Enter Date: "))
    date=datetime.date(Y,M,D)
    return date
menu()
