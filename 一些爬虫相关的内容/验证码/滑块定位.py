import cv2
def findmatchtemplate(filepathname, befindimage):
    def canny(filepathname, left=180, right=240):
        v = cv2.imread(filepathname)
        s = cv2.cvtColor(v, cv2.COLOR_BGR2GRAY)
        s = cv2.Canny(s, left, right)
        return s
    img1 = canny(filepathname)
    img2 = canny(befindimage)
    w, h = img1.shape[:2]
    v = cv2.matchTemplate(img2,img1,cv2.TM_CCOEFF)
    a, b, c, left_top = cv2.minMaxLoc(v)
    def accurate(left_top, canny_img1):
        s = canny_img1
        v = []
        for idx,i in enumerate(s):
            if any(i):
                v.append(idx)
        gt = v[0]
        h = v[-1] - v[0]
        s = s.T
        v = []
        for idx,i in enumerate(s):
            if any(i):
                v.append(idx)
        gl = v[0]
        w = v[-1] - v[0]
        t, l = left_top[1]+gt, left_top[0]+gl
        return t, l, w, h
    t, l, w, h = accurate(left_top, img1)
    def test():
        cv2.imshow('nier1', img1)
        cv2.imshow('nier2', img2)
        img3 = cv2.imread(befindimage)
        img3 = cv2.rectangle(img3, (l, t), (l+h, t+w), (0,255,0), 2)
        cv2.imshow('nier', img3); cv2.waitKey(); cv2.destroyAllWindows()
    test() # 使用时注释这行就可以了
    return t, l, w, h

s = findmatchtemplate('front.png', 'bg.jpg')
print(s)