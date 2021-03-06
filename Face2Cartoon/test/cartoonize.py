import os
import cv2
import numpy as np
import tensorflow as tf 

from tqdm import tqdm
import network
import guided_filter

class Model(object):
    def __init__(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.join(basedir,"..","model","saved_models")
        self.input_photo = tf.placeholder(tf.float32, [1, None, None, 3])
        network_out = network.unet_generator(self.input_photo)
        self.final_out = guided_filter.guided_filter(self.input_photo, network_out, r=1, eps=5e-3)

        all_vars = tf.trainable_variables()
        gene_vars = [var for var in all_vars if 'generator' in var.name]
        saver = tf.train.Saver(var_list=gene_vars)
        
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.session = tf.Session()

        self.session.run(tf.global_variables_initializer())
        saver.restore(self.session, tf.train.latest_checkpoint(model_path))

    def resize_crop(self,image):
        h, w, c = np.shape(image)
        if min(h, w) > 720:
            if h > w:
                h, w = int(720*h/w), 720
            else:
                h, w = 720, int(720*w/h)
        image = cv2.resize(image, (w, h),
                        interpolation=cv2.INTER_AREA)
        h, w = (h//8)*8, (w//8)*8
        image = image[:h, :w, :]
        return image
        
    def cartoonize(self,load_folder, save_folder):
        # basedir = os.path.abspath(os.path.dirname(__file__))
        # model_path = os.path.join(basedir,"..","model","saved_models")
        # 'D:/git/cvfall/Face2Cartoon/model/saved_models'
        #load_folder = 'C:/Users/user/Documents/GitHub/face_animation_ours/Face2Cartoon/test/test_images'
        #save_folder = 'C:/Users/user/Documents/GitHub/face_animation_ours/Face2Cartoon/cartoonized_images'

        # input_photo = tf.placeholder(tf.float32, [1, None, None, 3])
        # network_out = network.unet_generator(input_photo)
        # final_out = guided_filter.guided_filter(input_photo, network_out, r=1, eps=5e-3)

        # all_vars = tf.trainable_variables()
        # gene_vars = [var for var in all_vars if 'generator' in var.name]
        # saver = tf.train.Saver(var_list=gene_vars)
        
        # config = tf.ConfigProto()
        # config.gpu_options.allow_growth = True
        # sess = tf.Session(config=config)

        # sess.run(tf.global_variables_initializer())
        # saver.restore(sess, tf.train.latest_checkpoint(model_path))
        name_list = os.listdir(load_folder)
        for name in tqdm(name_list):
            try:
                load_path = os.path.join(load_folder, name)
                save_path = os.path.join(save_folder, name)
                image = cv2.imread(load_path)
                image = self.resize_crop(image)
                batch_image = image.astype(np.float32)/127.5 - 1
                batch_image = np.expand_dims(batch_image, axis=0)
                output = self.session.run(self.final_out, feed_dict={self.input_photo: batch_image})
                output = (np.squeeze(output)+1)*127.5
                output = np.clip(output, 0, 255).astype(np.uint8)
                cv2.imwrite(save_path, output)
            except:
                print('cartoonize {} failed'.format(load_path))


    def main(self,load_folder , save_folder):
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
            print(save_folder)
        print(load_folder)
        print(save_folder)
        self.cartoonize(load_folder, save_folder)


# if __name__ == '__main__':
#     load_folder = 'C:/Users/user/Documents/GitHub/face_animation_ours/Face2Cartoon/test/test_images'
#     save_folder = 'C:/Users/user/Documents/GitHub/face_animation_ours/Face2Cartoon/cartoonized_images'
#     if not os.path.exists(save_folder):
#         os.mkdir(save_folder)
#     cartoonize(load_folder, save_folder)


    