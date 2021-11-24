import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os,base64,threading,webbrowser

class API () :
    def Login () :
        PswGui=tk.Tk()
        PswGui.title('HTTPS Blocker ( Login )')
        PswGui.iconbitmap('icon.ico')
        PswGui.resizable(0,0)
        PswGui.geometry('250x80')

        PswVar=tk.StringVar(PswGui)
        PswState={'?':False}
        def LOGIN () :
            # C:\Users\MY-PC\AppData\Roaming
            Path=os.environ['USERPROFILE'] + os.sep +r'AppData'+os.sep+'Roaming'+os.sep+'HTTPSBLkR.data'
            File=open(Path,'r')
            PSW=File.read()[::-1]
            File.close()
            if str(PswVar.get()) == PSW :
                PswState['?']=True
                PswGui.destroy()
            else:
                messagebox.showerror('Wrong !!','Password is Wrong !!')
                PswState['?']=False

        F=tk.Frame(PswGui,bd=15)
        F.pack()
        tk.Label(F,text='Password :').pack(side=tk.LEFT)
        ttk.Entry(F,width=15,textvariable=PswVar).pack(side=tk.RIGHT)

        ttk.Button(PswGui,text='Login',command=LOGIN).pack(side=tk.BOTTOM)
        PswGui.mainloop()
        return PswState['?']
    def SetPassword () :
        PswGui=tk.Tk()
        PswGui.title('HTTPS Blocker ( Set Password )')
        PswGui.iconbitmap('icon.ico')
        PswGui.resizable(0,0)
        PswGui.geometry('250x80')

        PassVar=tk.StringVar(PswGui)
        def ChangPsw () :
            # C:\Users\MY-PC\AppData\Roaming
            Path=os.environ['USERPROFILE'] + os.sep +r'AppData'+os.sep+'Roaming'+os.sep+'HTTPSBLkR.data'
            File=open(Path,'w')
            File.write(str(PassVar.get())[::-1])
            File.close()
            messagebox.showinfo('Done',f'New Password is Set To "{str(PassVar.get())}" Successfully')
            PswGui.destroy()

        F=tk.Frame(PswGui,bd=15)
        F.pack()
        tk.Label(F,text='New Password :').pack(side=tk.LEFT)
        ttk.Entry(F,textvariable=PassVar,width=15).pack(side=tk.RIGHT)

        ttk.Button(PswGui,text='Set',command=ChangPsw).pack(side=tk.BOTTOM)
        PswGui.mainloop()
        return
    def ReadHosts (LISTBOX):
        for i in open(r'C:\Windows\System32\drivers\etc\hosts','r').read().splitlines():
            if (i.startswith('#')) or (i.strip()==''):
                continue
            Cmnd=i.split(' ')
            LISTBOX.insert(0,' '+Cmnd[len(Cmnd)-1])

class GuiApp ():
    def __init__ (self,root):
        root.geometry('450x200')
        root.title('HTTPS Blocker')
        root.iconbitmap('icon.ico')

        # Variables
        URL=tk.StringVar()

        # Text Bar
        def placeholder (varr):
            if str(URL.get()) == '< URL Here >': URLBar.delete(0, tk.END)
            else:print()
        URLBar=ttk.Entry(width=71,textvariable=URL)
        URLBar.place(x=7,y=20)
        URLBar.bind("<Button>",placeholder)
        URLBar.insert(0,'< URL Here >')

        # Buttons
        def Add () :
            UrlStr=str(URL.get()).strip()
            if not(('https://' in UrlStr) or ('http://' in UrlStr) or ('www.' in UrlStr)):
                messagebox.showerror('Erorr !!','Please Tybe Full Url [ Ex: https://www.instagram.com ]')
                return
            if UrlStr in list(listbox.get(0,last=10000)):
                messagebox.showerror('Error !!','This URL is Already Added ..')
                return
            listbox.insert(0,UrlStr)
        def Remove () :
            listbox.delete(tk.ANCHOR)
        def Update () :
            AllWebsites=list(listbox.get(0,last=10000))
            FinalWebsites=[]
            # Translate URL Syntax
            for data in AllWebsites:
                if data.startswith(' '):
                    FinalWebsites.append('127.0.0.1 '+data.strip())
                    continue
                S=data.replace('https://','').replace('http://','')
                if 'www.' in S:
                    with_www=str(S)
                    without_www=S.replace('www.','')
                    FinalWebsites.append('127.0.0.1 '+with_www)
                    FinalWebsites.append('127.0.0.1 '+without_www)
                else:
                    FinalWebsites.append('127.0.0.1 '+S)
            
            # C:\Windows\System32\drivers\etc\hosts
            README=[]
            for data in open(r'C:\Windows\System32\drivers\etc\hosts','r').read().splitlines():
                if (data.startswith('#')) or (data.strip()==''):
                    README.append(data)
            
            try:
                Hosts=open(r'C:\Windows\System32\drivers\etc\hosts','w')
                Hosts.write('\n'.join(README)+'\n')
                Hosts.write('\n'.join(FinalWebsites))
                Hosts.close()
                messagebox.showinfo('Done !!','Blocked List Has Updated ..')
            except Exception as AdminErr:
                ERROR=str(AdminErr)[:str(AdminErr).find(':')+1]+" 'HOSTS_FILE'"
                messagebox.showerror('Admin Error !!',f'Please Run Program as Admin :\n{ERROR}')
        addBtn=ttk.Button(root,text='Add',command=Add)
        addBtn.place(x=7,y=50)

        removeBtn=ttk.Button(root,text='Remove',command=Remove)
        removeBtn.place(x=95,y=50)

        updateBtn=ttk.Button(root,text='Update',command=Update)
        updateBtn.place(x=185,y=50)

        helpBtn=ttk.Button(root,text='Help',command=lambda:webbrowser.open("http://zaky.eu5.org/HTTPSBlocker/"))
        helpBtn.place(x=270,y=50)

        pswBtn=ttk.Button(root,text='Set Password',command=API.SetPassword)
        pswBtn.place(x=360,y=50)

        # Sites List
        listbox = tk.Listbox(root,width=71,height=5)
        listbox.place(x=7,y=90)
        API.ReadHosts(listbox)


if __name__ == '__main__':
    Path=os.environ['USERPROFILE'] + os.sep +r'AppData'+os.sep+'Roaming'+os.sep+'HTTPSBLkR.data'
    try:
        open(Path,'r')
        SS=API.Login()
        if SS:
            TKGui=tk.Tk()
            TKGui.resizable(0,0)
            GuiApp(TKGui)
            TKGui.mainloop()
    except:
        TKGui=tk.Tk()
        TKGui.resizable(0,0)
        GuiApp(TKGui)
        TKGui.mainloop()