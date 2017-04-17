
import PIL
from PIL import Image

def resize(width, path):
    img = Image.open(path)
    wpercent = (width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((width, hsize), PIL.Image.ANTIALIAS)
    img.save(path)


def do_array(path):           
    temp=Image.open(path)
    temp=temp.convert('1')      # Convert to black&white
    A = np.array(temp)             # Creates an array, white pixels==True and black pixels==False
    new_A=np.empty((A.shape[0],A.shape[1]),None)    #New array with same size as A

    for i in range(len(A)):
        for j in range(len(A[i])):
            if A[i][j]==True:
                new_A[i][j]=0
            else:
                new_A[i][j]=1
    return new_A
