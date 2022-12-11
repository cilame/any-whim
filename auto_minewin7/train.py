from CreateCate import CreateCate
s = CreateCate('pic')
s.save_mapdict('mycate_model.pickle')

x = s.x/255.
y = s.y

import keras
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import Sequential

def mkmodel(shape,classnum):
    model = Sequential()
    model.add(Conv2D(9,(3,3), padding="same", activation='relu', input_shape=shape))
    model.add(MaxPooling2D(2,2,padding="same"))

    model.add(Flatten())
    model.add(Dense(20, activation='relu'))
    model.add(Dense(classnum, activation='softmax'))

    model.compile('adam','categorical_crossentropy',metrics=['accuracy'])
    return model

model = mkmodel(s.x.shape[1:],s.class_num)
print 'train-------'
model.fit(x,y,epochs=100)
model.save('mytrain_model.h5')

print '\ntrain_ok-------'
loss,accuracy = model.evaluate(x,y)
print 'loss:',loss
print 'accuracy:',accuracy
