import cv2 as cv
import imutils
import time
from datetime import datetime
import numpy as np
from picamera2 import  *
from star_detect import is_star
from os import system
import star_location_by_gps


class VideoCamera(object):
    def __init__(self, flip = False, file_type  = ".jpg", photo_string= "astro_unique_photo", file_dat="star_coord_obj/data.skycoord"):
        self.vs = picamera2.Picamera2(0)
        config = self.vs.create_preview_configuration({'format': 'RGB888'})
        self.vs.configure(config)
        self.vs.start()
        self.flip = flip 
        self.file_type = file_type 
        self.photo_string = photo_string 
        time.sleep(2.0)

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self) -> bytes:
        
        frame = self.flip_if_needed(self.vs.capture_array())
        img_preproc = cv.cvtColor(frame, cv.COLOR_RGBA2RGB)
        ret, jpeg = cv.imencode(self.file_type, img_preproc)
        if not ret:
            print(f"failed to grab frame on read")
            return bytes((0))
                
        ret, jpeg = cv.imencode(self.file_type, frame)
        if not ret:
            print("failed to grab frame on encode")
            return bytes((0))
        
        frame = self.flip_if_needed(frame)

        self.previous_frame = jpeg
        return jpeg.tobytes()
    
    def take_picture(self):
        frame = self.flip_if_needed(self.vs.capture_array())
        img_preproc = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
        ret, jpeg = cv.imencode(self.file_type, img_preproc)
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S") 
        if is_star(frame):
            file_tmp = cv.imwrite(str("photos/" + self.photo_string + "_" + today_date + self.file_type + "_tmp"), frame)
            file1=f'star_catalog/database_{i}'
            with open(self.file_dat, "rb") as data_storage:
                skycoord_f = pickle.load(data_storage)
                astro_search_star(skycoord_f, file_tmp, file1)
            data_storage.close()
        cv.imwrite(str(self.photo_string + "_" + today_date + self.file_type), frame)
    
    def take_timelapse(self, sec, hour):
        dateraw= datetime.now()
        datetimeformat = dateraw.strftime("%Y-%m-%d_%H:%M")
        num_photos = int((int(hour)*3600)/int(sec))
        for i in range(num_photos):
            frame = self.flip_if_needed(self.vs.capture_array())
            img_preproc = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
            ret, jpeg = cv.imencode(self.file_type, img_preproc)
            cv.imwrite("timelapse/" + str(self.photo_string + "_" + str(i) + self.file_type), frame)
            time.sleep(int(sec))
        system('ffmpeg -r {} -f image2 -s 1024x768 -nostats -loglevel 0 -pattern_type glob -i "timelapse/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p {}.mp4'.format(fps, datetimeformat))

    def star_detection(self, n):
        n = n * 3600
        for i in range(n):
            frame = self.flip_if_needed(self.vs.capture_array())
            img_preproc = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
            ret, jpeg = cv.imencode(self.file_type, img_preproc)
            if is_star(frame):
                file_tmp = cv.imwrite("tmp/frame_{}.jpg", frame).format(i)
                file1=f'star_catalog/database_{i}'
                with open(self.file_dat, "rb") as data_storage:
                    skycoord_f = pickle.load(data_storage)
                    astro_search_star(skycoord_f, file_tmp, file1)
        data_storage.close()

                