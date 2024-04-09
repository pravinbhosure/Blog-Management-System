from django.shortcuts import render,redirect
from django.contrib import messages
from django.db import connection
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout
from django.http import JsonResponse



conn = connection
cursor = conn.cursor()




def login_page(request):
    '''
    function get Email, and Password from loginform.html page and check email and password is valid or not
    Function redirect a home page if all process does not generate error
    Function return a same page if any error exists
    '''
    try:
        if request.method == 'POST':
            Em = request.POST.get('Email')
            Pwd = request.POST.get('Password')
            #set session for email
            request.session['Email'] = Em
            

            get_query = "select * from login_TB where email = '{}' and password = '{}'".format(Em,Pwd) 
            cursor.execute(get_query)
            t = tuple(cursor.fetchone())
            if t == ():
                messages.error(request,"Invalid Email or Password....")
                return render(request,'loginform.html')
            else:
                name = t[1] 
                #set session for name
                request.session['name'] = name
                return redirect(home)

        return render(request,"loginform.html")
    except:
        messages.error(request,"Invalid Email or Password....")
        return render(request,"loginform.html")
    finally:
        conn.close()


def register(request):
    '''
    function generate own id
    function get Name, Email, and Password from register.html page and insert the data into login_tb table
    Function return a Login  page if all process does not generate error
    Function return a same page if any error exists
    '''
    try:
        if request.method == 'POST':
            # for get id
            query_id = "select max(id) from login_TB"
            cursor.execute(query_id)
            mx = cursor.fetchone()
            # generate id
            if mx == ():
                id = 1
            else:
                id = int(mx[0]) + 1

            fn = request.POST.get('Name')
            Em = request.POST.get('Email')
            Pwd = request.POST.get('Password')
            #Insert the data into Login_Tb table
            c = "insert into login_TB values('{}','{}','{}','{}')".format(id,fn,Em,Pwd)
            cursor.execute(c)
            conn.commit()
            return render(request,"loginform.html")
        
        return render(request,"register.html")
    except:
        return render(request,"register.html")
    finally:
        conn.close()

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    '''
    function fetch data from blog_details table and send to the home.html page
    Function return a home.html if all process does not generate error
    ''' 
    if 'Email' in request.session:  
        cursor.execute("SELECT * FROM blog_details WHERE Email='{}'".format(request.session['Email']))
        myresult = cursor.fetchall()
        return render(request,'home.html',{'name':request.session['name'],'myresult':myresult})
    else:
        return redirect('register_form')

    
def Blog(request):
    """
    function get data from add_blog pop model. and insert to blog_details table
    Function redirect a home.html if process does not generate error
    """    
    if request.method == 'POST':
        date = request.POST.get('date')
        blog = request.POST.get('blog')
        insert_query ="INSERT INTO Blog_Details (Email,date,task) VALUES ( '{}','{}','{}')".format(request.session['Email'],date,blog)
        cursor.execute(insert_query)
        conn.commit()
        return redirect(home)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_activity(request):
    """
    function fetch data from login_Tb table and send to the Login_Activity page
    Function render Login_Activity.html if process does not generate error
    """
    if 'Email' in request.session: 
        cursor.execute("SELECT * FROM login_TB ")
        myresult = cursor.fetchall()
        return render (request,'Login_Activity.html',{'name':request.session['name'],'myresult':myresult})
    else:
        return redirect('register_form')
        

def update(request):
    '''
    function get data from update_Blog pop model. and update to blog_details table
    Function redirect a home.html if process does not generate error
    '''
    if request.method == 'POST':
        id = request.POST.get('Id')
        blog  = request.POST['Blog'] 
        update_blog = "update blog_details set task = '{}' where id = '{}'".format(blog,id) 
        cursor.execute(update_blog)
        conn.commit()
        return redirect(home)
        

def delete(request):
    '''
    function get id and delete from blog_details table
    Function redirect a home.html if process does not generate error
    '''
    if request.method == 'POST':
        id = request.POST.get('id')  
        print("146 ===",id)
        del_query ="DELETE FROM Blog_Details WHERE id='{}'".format(id)
        cursor.execute(del_query)
        conn.commit()
        return redirect(home)

def update_user(request):
    '''
    function get data from update_user pop model. and update to login_Tb table
    Function redirect a login_activity if process does not generate error
    '''
    if request.method == 'POST':
        id = request.POST.get('id')
        uname  = request.POST['Username']
        Email  = request.POST['Email']
        up_query = "update login_TB set Name = '{}',Email = '{}' where id = '{}'".format(uname,Email,id) 
        cursor.execute(up_query)
        conn.commit()
        return redirect(login_activity)

def delete_user(request):
    '''
    function get id and delete from Login_Tb table
    Function redirect a login_activity if process does not generate error
    '''
    if request.method == 'POST': 
        id = request.POST.get('id')
        del_query ="DELETE FROM login_TB WHERE id='{}'".format(id)
        cursor.execute(del_query)
        conn.commit()
        return redirect(login_activity)

def logout_view(request):
    try:
        #del request.session['Email']
        #del request.session['name']
        logout(request)
        return redirect(register)
    except:
        return redirect(register)




def get_user_data(request):
    """
    update user details
    get the data from login table and return json response 
    """
    print("214-----------------------------------------------")      
    update_team_id = request.GET.get('id', None) 
    print("_______________________",update_team_id)

    try:
        data = []
        cursor.execute("SELECT * FROM login_TB WHERE id='{}'".format(update_team_id))
        #data1 =cursor.fetchone()   
        #print("data1",data1)
        #print("195--",cursor.description)
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))

        print("result++++++++team++++++++++++",data)

    except:
        messages.success(request, f'Data not insert please try again !!!')
    finally:
        if not conn:
            conn.close()  
        return JsonResponse(data[0],  content_type="application/json" ,safe=False)
       

def get_data(request):
        """
        for the blog details
        get the data from blog table and return json response
        
        """
        #print("183-----------------------------------------------")      
        update_team_id = request.GET.get('id', None) 
        #print("_______________________",update_team_id)

        try:
            data = []
            cursor.execute("SELECT * FROM blog_details WHERE id='{}'".format(update_team_id))
            #data1 =cursor.fetchone()   
            #print("data1",data1)
            #print("195--",cursor.description)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))

            print("result++++++++team++++++++++++",data)

        except:
            messages.success(request, f'Data not insert please try again !!!')
        finally:
            if not conn:
                conn.close()  
        return JsonResponse(data[0],  content_type="application/json" ,safe=False)
       

