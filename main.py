from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import socket
from flask import Flask, Response, make_response, request
import sys
import qrcode, os
import random
 
app = Flask(__name__)
#my local ip adress
my_ip = socket.gethostbyname(socket.gethostname())
select_file = []
file_n = 0

server_port = random.randint(0,9999)

#make a qrcode
file_name = "qr_code.png" #qr code file
qr_string = "http://" + str(my_ip) + ":" +str(server_port) + "/"
img = qrcode.make(qr_string) #Make qrcode
img.save(file_name)	#Save a images
current_dir = os.getcwd() #Save the this directory
print("fond error!") # no error!

html = ""

#get file name
def file_name(file):
    name = ""
    n = len(file)
    print(file[n-1])
    print(file)
    while True:
        if file[n-1] ==  '/' :
            name = file[n:len(file)]
            break
        
        if n == 1:
            break
        
        n = n - 1
        pass
    print(name)
    return name

#requests my_ip:port/
@app.route('/')
def index():
    return html

@app.route("/download")
def download():
    global select_file
    global file_n
    file_n = int(request.args.get("f")) #file number
    response = make_response()
    response.data  = open(select_file[file_n], "rb").read()
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename='+file_name(select_file[file_n])+''
    return response

def file_select():
    global select_file
    filetype = [("すべて","*")]
    file_path = tk.filedialog.askopenfilename(filetypes = filetype, initialdir = "")
    file_box.insert(tk.END,file_path)
    if file_path != "":
        select_file.append(file_path)
        pass
    pass

def file_share():
    global root
    global html
    global select_file
    
    if select_file == []:
        res = messagebox.showerror("error", "ファイルが選択されていません。")
    else:
        download_list = ""
        for n in range(len(select_file)):
            download_list = download_list + '''
        <h3><svg version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 512 512" style="width: 64px; height: 64px; opacity: 1;" xml:space="preserve">
        <g>
	<path class="st0" d="M503.283,233.406c-8.198-11.548-21.106-18.678-35.108-19.704v-44.571c0.007-12.334-5.052-23.663-13.14-31.724
		c-8.068-8.088-19.39-13.14-31.724-13.134H220.167c-2.495,0-4.916-0.951-6.755-2.681l0.013,0.021L177.73,88.139
		c-8.321-7.794-19.287-12.136-30.684-12.136H88.698c-12.334-0.007-23.663,5.053-31.724,13.141
		c-8.088,8.06-13.147,19.39-13.14,31.724v92.834c-14.002,1.026-26.911,8.156-35.109,19.711C2.981,241.509,0,251.094,0,260.768
		c0,5.244,0.875,10.53,2.66,15.616l42.15,120.524c0.247,0.69,0.499,1.299,0.821,1.956c1.935,3.917,3.74,7.766,5.77,11.609
		c3.07,5.695,6.584,11.78,12.943,17.14c3.158,2.632,7.035,4.888,11.253,6.317c4.225,1.443,8.676,2.072,13.1,2.066H423.31
		c7.302,0.04,14.18-2.352,19.349-5.71c7.849-5.086,12.491-11.568,16.032-17.202c3.48-5.647,5.894-10.905,7.412-13.688
		c0.486-0.916,0.746-1.511,1.087-2.488l42.157-120.531c1.778-5.08,2.653-10.365,2.653-15.609
		C512,251.094,509.026,241.509,503.283,233.406z M433.168,213.497H78.838v-92.628c0.007-2.776,1.074-5.128,2.885-6.974
		c1.846-1.812,4.198-2.878,6.974-2.885h58.348c2.509,0,4.908,0.951,6.748,2.667l35.69,33.468l0.013,0.02
		c8.3,7.76,19.26,12.115,30.671,12.115H423.31c2.776,0.006,5.134,1.074,6.974,2.885c1.812,1.839,2.879,4.191,2.885,6.967V213.497z" style="fill: rgb(0, 70, 255);"></path>
</g>
</svg>
                <a href="download?f='''+str(n)+'''">'''+file_name(select_file[n])+'''</a></h3>
'''
            pass
        html = '''
        <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width">
            </head>
        
            <body>
                <h1>ファイル共有</h1>
<style type="text/css">
	.st0{fill:#4B4B4B;}
</style>
            '''+download_list+'''
            </body>
        </html>

        '''
        root.destroy()
    pass

#run 
if __name__ == '__main__':
    #ui
    root = tk.Tk()
    root.title("ファイル転送")
    root.geometry("600x400")

    file_box = tk.Entry(width=40)
    file_box.place(x=10,y=100)
    
    file_label = tk.Label(text="File")
    file_label.place(x=10,y=70)
    #file select button
    file_button = tk.Button(text="選択",command=file_select,font=("UTF-8",10))
    file_button.place(x=10,y=130)

    #share button
    share_button = tk.Button(text="共有(このウィンドウを閉じる)",command=file_share, font=("UTF-8",10))
    share_button.place(x=100,y=130)

    #use infomation
    use_info = tk.Label(text='''使い方 :① [参照]ボタンを押してファイルを選ぶ 。
②スマホで表示されているQRコードを読み込む
③[共有(ウィンドウを閉じる)]ボタンを押す
④スマホからQRコードのURLにアクセスする''')
    use_info.place(x=0,y=180)
    
    #share explanation
    share_letter = tk.Label(text='''注意 : 携帯などの端末でQRコードを読み取っても、
[共有(ウィンドウを閉じる)]ボタンを押
さないとファイルは共有されません。

ファイルを共有するときは、共有する端末と同じ
ルーターに接続してください。''',font=("UTF-8",10),foreground="#ff0000")
    share_letter.place(x=0,y=250)

    #Display qrcode
    qr_code_img = tk.PhotoImage(file="qr_code.png")
    canvas = tk.Canvas(bg="black", width=500, height=500)
    canvas.place(x=280, y=70)
    canvas.create_image(0, 0, image=qr_code_img, anchor=tk.NW)

    #Prohibition of window resizing
    root.resizable(0,0)
    
    #mainloop
    root.mainloop()

    #run
    app.run(debug=False, host=my_ip, port=server_port)
    pass
