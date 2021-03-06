from keras.layers import Input, Concatenate
from keras.models import Model
import keras.backend as K
from keras.applications.vgg19 import VGG19,preprocess_input


def perceptual_loss_fine(y_true, y_pred):
    y_true = ((y_true + 1) / 2)#* 255.0
    y_pred = ((y_pred + 1) / 2)# * 255.0
    input_layer = Input((512,512,1))
    tripleOut = Concatenate()([input_layer,input_layer,input_layer])
 
    vgg = VGG19(include_top=False, weights='imagenet', input_shape=(512,512,3))
    out1 = vgg.get_layer('block1_conv2').output
    out2 = vgg.get_layer('block2_conv2').output
    out3 = vgg.get_layer('block3_conv4').output
    out4 = vgg.get_layer('block4_conv4').output
    out5 = vgg.get_layer('block5_conv4').output
    loss_model = Model(vgg.input, [out1,out2,out3,out4,out5])
    loss_model.trainable = False
 
 
    loss_model_output =  loss_model(tripleOut)
    final_model = Model(input_layer, loss_model_output)
    final_model.trainable = False
    vgg_x = final_model(y_true)
    vgg_y = final_model(y_pred)
 
    perceptual_weights = [1.0/32, 1.0/16, 1.0/8, 1.0/4, 1.0]
    #perceptual_weights = [1.0, 1.0, 1.0, 1.0, 1.0]
    perceptual_loss = 0
    for i in range(len(vgg_x)):
        perceptual_loss += perceptual_weights[i] * K.mean(K.square(vgg_x[i] - vgg_y[i]))
    return perceptual_loss
def perceptual_loss_coarse(y_true, y_pred):
    y_true = ((y_true + 1) / 2)# * 255.0
    y_pred = ((y_pred + 1) / 2)# * 255.0
    input_layer = Input((256,256,1))
    tripleOut = Concatenate()([input_layer,input_layer,input_layer])
 
    vgg = VGG19(include_top=False, weights='imagenet', input_shape=(256,256,3))
    out1 = vgg.get_layer('block1_conv2').output
    out2 = vgg.get_layer('block2_conv2').output
    out3 = vgg.get_layer('block3_conv4').output
    out4 = vgg.get_layer('block4_conv4').output
    out5 = vgg.get_layer('block5_conv4').output
    loss_model = Model(vgg.input, [out1,out2,out3,out4,out5])
    loss_model.trainable = False
 
 
    loss_model_output =  loss_model(tripleOut)
    final_model = Model(input_layer, loss_model_output)
    final_model.trainable = False
    vgg_x = final_model(y_true)
    vgg_y = final_model(y_pred)
 
    perceptual_weights = [1.0/32, 1.0/16, 1.0/8, 1.0/4, 1.0]
    perceptual_loss = 0
    for i in range(len(vgg_x)):
        perceptual_loss += perceptual_weights[i] * K.mean(K.square(vgg_x[i] - vgg_y[i]))
    return perceptual_loss
 
def ef_loss(y_true, y_pred):
    ef_loss = 0
    for i in range(len(y_true)):
        ef_loss += K.mean(K.abs(y_true[i] - y_pred[i]))
    return ef_loss
