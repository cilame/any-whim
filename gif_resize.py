from PIL import Image
import sys

def get_gif(infile,mode="RGBA",save=False):
    p = []
    try:
        im = Image.open(infile)
    except IOError:
        print ("Cant load", infile)
        sys.exit(1)
    i = 0
    mypalette = im.getpalette()
    try:
        while 1:
            im.putpalette(mypalette)
            new_im = Image.new(mode, im.size)
            new_im.paste(im)
            if save:
                new_im.save('image\\a'+str(i)+'.png')
            else:
                p.append(new_im)
            i += 1
            im.seek(im.tell() + 1)
    except EOFError:
        pass # end of sequence
    return p

def resize_gif(name,images,size,step=1):
    q = []
    for idx,i in enumerate(images[::step]):
        if isinstance(size,(tuple,list)):
            q.append(i.resize(size))
        elif isinstance(size,(int,float)):
            width = int(i.width/size)
            height = int(i.height/size)
            q.append(i.resize((width,height)))
    q[0].save(name,
              save_all=True,
              append_images=q[1:],
              loop=10000,
              duration=1,
              comment=b"aaabb")
    print(size)

s = get_gif('./xxx.gif')
resize_gif('gif.gif',s,3/1.75,4)
