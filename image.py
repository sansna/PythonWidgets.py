from PIL import Image
img = Image.open('code.jpg')
nimg=img.transform((img.width+10,img.height+20),Image.AFFINE,(1,-1,0,-0.1,1,0),Image.BILINEAR)
nimg.convert('RGBA') # this seems not working ..
a,b,c=nimg.split()
iter_a=a.getdata()
newa=[]
for aitem in iter_a:
    newa.append(100)
a.putdata(newa)
nimg.putalpha(a) # Forcing file mode to RGBA..
datas=nimg.getdata()
newData=[]
i=0
for item in datas:
    if item[0]==0 and item[1]==0 and item[2] == 0:
        newData.append((0,0,0,0))
    else:
        newData.append(item)
        Image.Image.putdata
nimg.putdata(newData)
nimg.save('hell.png') # it is said to be transparent, .. but I did not make it..
#Now it is working..
