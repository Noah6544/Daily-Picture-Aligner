import numpy as np
import mediapipe as mp
import cv2 as cv
import traceback

mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
drawing_spec = mp_drawing.DrawingSpec(thickness=0, circle_radius=1)

ErrorFile = open("ErrorLog.txt","a")

left_eye_landmark = 468 # 468 is left eye
right_eye_andmark = 473 # 473 is right eye

class Image:
    def scale_down_image(self):
        # For some reason, if an image is too large, there seems to be some landmark detection
        # issues, therefore, we scale the image down by 2
        if self.width > self.height and (self.height >= 3024 or self.width >= 4032):

            self.height, self.width = int(self.cvimage.shape[0] / 2),int(self.cvimage.shape[1] / 2)

            # Divide by 2 here, and not above, for some reason, this makes sure it is an int and not a float!
            self.dimensions = (self.width, self.height)

            # Leave it at (0,0) it seems to work better for 1 base image alignments. idk why YET
            matrix = cv.getRotationMatrix2D( (0,0), 0, 0.5)

            # Warp affine last tuple argument must be floats!!
            self.cvimage = cv.warpAffine(self.cvimage, matrix, self.dimensions)
            self.refresh_eye_coordinates()
            return self.cvimage


    def __init__(self, lib_file, corresponding_base_image=None, confidence=0.2):
        self.ultimate_angle = None
        self.ultimate_translate_y = None
        self.ultimate_translate_x = None
        self.ultimate_scale_factor = None
        self.confidence = confidence
        self.scale_factor = None
        self.left_eye_x = None
        self.left_eye_y = None
        self.right_eye_x = None
        self.right_eye_y = None
        self.y_difference = None
        self.x_difference = None
        self.current_image_coordinates = None

        self.lib_file = lib_file
        self.name = lib_file.name
        self.cvimage = cv.imread(str(lib_file))
        
        # Convert to format with alpha channel
        self.cvimage = cv.cvtColor(self.cvimage, cv.COLOR_BGR2BGRA)
        self.height, self.width = self.cvimage.shape[:2]
        self.dimensions = (self.width, self.height)

        self.scale_down_image()

        self.left_eye_image_coordinates = self.get_image_coordinates(left_eye_landmark)
        self.right_eye_image_coordinates = self.get_image_coordinates(right_eye_andmark)

        # Straight from stack overflow
        self.corresponding_base_image = corresponding_base_image if corresponding_base_image is not None else None
        try:
            self.left_eye_x, self.left_eye_y = self.left_eye_image_coordinates[0],self.left_eye_image_coordinates[1]
            self.right_eye_x, self.right_eye_y = self.right_eye_image_coordinates[0],self.right_eye_image_coordinates[1]
            self.y_difference = self.right_eye_y - self.left_eye_y
            self.x_difference = self.right_eye_x - self.left_eye_x
        except Exception as error:
            # Don't mask errors
            print(str(error))
            pass

    def __str__(self):
        try:
            print("Shape: ", self.cvimage.shape)
            print("XdifferneceNomral = ",self.x_difference)
            print("LeftEyeImageCoordinates: ", self.left_eye_image_coordinates)
            print("RightEyeImageCoordinates: ", self.right_eye_image_coordinates)
            print("UltimateScalefactor: ",self.ultimate_scale_factor)
            print("UltimateTranslateX: ",self.ultimate_translate_x)
            print("UltimateTranslate Y:",self.ultimate_translate_y)
            print("UltimateAngle: ",self.ultimate_angle)
            return "OK"
        except Exception as error:
            # Handle error logic within the align_image_to_base_image class
            # Don't mask errors
            print(str(error))
            return ""


    def get_image_coordinates(self, target_landmark):
        try:
            with (mp_face_mesh.FaceMesh(static_image_mode=True,
                                       max_num_faces=2,
                                       refine_landmarks=True,
                                       min_detection_confidence=self.confidence)
                  as face_mesh):
               
                # Convert the BGR image to RGB and process it with MediaPipe Face Detection
                results = face_mesh.process(cv.cvtColor(self.cvimage, cv.COLOR_BGR2RGB))

                # If there are no face landmarks detected, return 'None'
                if not results.multi_face_landmarks:
                    return None
                
                # Print and draw face mesh landmarks on image
                for face_landmarks in results.multi_face_landmarks:     
                    for id, landmark in enumerate(face_landmarks.landmark):
                        
                        # Return early if not the landmark we want
                        if id == target_landmark:
                            self.current_image_coordinates = [landmark.x * self.width, landmark.y * self.height,
                                                              landmark.z]
                            if self.current_image_coordinates is None:
                                raise error
                            return self.current_image_coordinates
                        else:
                            pass
                            

        except Exception as error:
            # Handle error logic within the align_image_to_base_image class
            # Don't mask errors
            print(str(error))
            pass

    def refresh_eye_coordinates(self): #this is needed because after the transformations, the eye locations change! #updated so that it does the transformations with basic math. saves so much computational time.
        try:
            # self.LeftEyeImageCoordinates = self.getImageCoordinates(468) #for the webcam alignment, this is horrendously slow. like 2fps.
            # self.RightEyeImageCoordinates = self.getImageCoordinates(473) #and then to make it worse, we do it again for another eye.
            self.left_eye_x, self.left_eye_y = self.left_eye_x * self.scale_factor, self.left_eye_y * self.scale_factor
            self.right_eye_x, self.right_eye_y = self.right_eye_x * self.scale_factor, self.right_eye_y * self.scale_factor
            self.x_difference = self.right_eye_x - self.left_eye_x
        except Exception as error:
            # Handle error logic within the align_image_to_base_image class
            # Don't mask errors
            print(str(error))
            pass

    # This function scales the image by a calculated scalefactor to remove and differences in camera distance
    def scale_around_point(self, base_image):
        try:
            # A very simply formula I came up with, wasn't my first iteration, but it works now. I'm saying
            # that like it's complex math, it's literally a fraction ratio
            self.scale_factor = (base_image.x_difference / self.x_difference)

            # (0,0)=x-y coord, 0=rotation angle, self.scale_factor=scaling factor
            # scale from the center of img
            matrix = cv.getRotationMatrix2D( (0,0) , 0, self.scale_factor)

            # Multiplying by 2 to ensure the entire image stays in frame, then on the rotation (the final
            # transformation) we scale it back down to normal to ensure none of hte image gets cut off!
            self.cvimage = cv.warpAffine(self.cvimage, matrix, self.dimensions)

        except Exception as error:
            # Handle error logic within the align_image_to_base_image class
            # Don't mask errors
            print(str(error))
            pass

    # This function simply shifts the image so that the left eye aligns with the base images left eye.
    def translate(self, x, y):
        trans_mat = np.float32([[1,0,x],[0,1,y]])

        # Manually updating them because it'll save some computational time in refreshing the images
        self.left_eye_x += x
        self.left_eye_y += y
        self.right_eye_x += x
        self.right_eye_y += y
        self.cvimage = cv.warpAffine(self.cvimage, trans_mat, self.dimensions)


    # This function rotates the image so that the slope of the eyes will align with the slope of
    # the base image, if that makes sense. if it doesn't it just makes it better trust me.
    def rotate_image(self, base_image):
        # Consider testing with Baseimage eye coordinates
        eye_point = (self.left_eye_x, self.left_eye_y)

        # Tangent formula right triangle.
        angle = np.rad2deg(np.arctan((self.right_eye_y - base_image.right_eye_y) / self.x_difference))
        rotational_matrix = cv.getRotationMatrix2D(eye_point, angle, 1.0)

        # We use the base image's width and height in case there are different sizes, so for base image, use
        # your smallest camera resolution photo. I took some with webcam and my phone for example, if I use my
        # webcam image as base image, my phone will be properly scaled down.
        self.cvimage = cv.warpAffine(self.cvimage, rotational_matrix, self.dimensions)

        # this is the inverse scale factor. THanks Dr. Garner.
        ### finalMatrix = cv.getRotationMatrix2D((0,0) , 0, 1/self.scale_factor)

        # Multiplying by 2 to ensure the entire image stays in frame, then on the rotation (the final
        # transformation) we scale it back down to normal to ensure none of hte image gets cut off!
        ### self.cvimage = cv.warpAffine(self.cvimage, finalMatrix,self.Dimensions)
        return angle


    def align_image_to_base_image(self, base_image):   #eyePoint = (BaseImage.LeftEyeX,BaseImage.LeftEyeY)
        # noinspection PyBroadException
        try:
            initial_x, initial_y = (base_image.left_eye_x, base_image.left_eye_y)
            self.scale_around_point(base_image)
            self.refresh_eye_coordinates()
            move_x = initial_x - self.left_eye_x
            move_y = initial_y - self.left_eye_y

            # TODO: Consider doing another final translation? cuz translate should come last after
            #  scaling the image back down but this is just experimental.
            self.translate(move_x,move_y)

            # This MUST come last. idk why, but try flipping translate and rotate and see how wonky it gets.
            angle = self.rotate_image(base_image)

            # This is a check to see if we have only 1 baseimage, this is the only time this wouldn't
            # be equal if we have 1 base image for image of differing resolutions. It saves us throwing in
            # an extra argument like "1baseimage" boolean, etc.
            if self.dimensions != base_image.dimensions:
                # Crop the image down. or not.
                self.cvimage = self.cvimage[0:base_image.height, 0:base_image.width]
                # If you're having funky results, make sure your base image matches the smallest image resolutions out of all other
                # images in your folder!
                pass

            # TODO: consider putting a crop if the dimensions are smaller, and not doing anything
            #  if the dimensions are larger
            return True

        except Exception as error:
            line = ''.join(['-' for i in range (28)])
            
            ErrorFile.write("\nAn Error Occurred. File is: \n'"
                            + self.name
                            + "'\nIt is likely that:"
                              "\n1. No face was found"
                              "\n2. A scaling issue occurred."
                              "\nCheck out the error:\n"
                            + traceback.format_exc() + line +"\n")
            return False


    def add_blur(self, original_image_path):
        h, w = self.cvimage.shape[:2]

        background = cv.imread(original_image_path)
        background = cv.resize(background, (w, h), interpolation = cv.INTER_LANCZOS4)

        # Kernel size for blurring
        ksize = (300, 300)
        background = cv.blur(background, ksize)

        # Separate the alpha channel from the color channels
        alpha_channel = self.cvimage[:, :, 3] / 255  # convert from 0-255 to 0.0-1.0
        overlay_colors = self.cvimage[:, :, :3]

        alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
        background_subsection = background[0:h, 0:w]

        # Combine the background with the overlay image weighted by the alpha channel
        composite = background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask

        # Overwrite the section of the background image that has been updated
        background[0:h, 0:w] = composite

        self.cvimage = background


class BaseImage(Image):
    def __init__(self, lib_file):
        super().__init__(lib_file)
        #ultimately, what we need is:
        self.ultimate_angle = None
        self.ultimate_scale_factor = None
        self.ultimate_translate_y = None
        self.ultimate_translate_x = None
        self.exact_x_difference = None
        self.ultimate_base_image_width = None
        self.ultimate_dimensions = None
        self.ultimate_base_image_height = None
        self.translate_x = None
        self.translate_y = None
        self.scale_factor= None
        self.angle = None


    # Basically calling the __init__ again, similar to making a new instance, this
    # is just for the alignment info function to reset stats.
    def reset(self):
        self.name = self.lib_file.name
        self.cvimage = cv.imread(str(self.lib_file))
        self.height, self.width = self.cvimage.shape[:2]
        self.dimensions = (int(self.width),int(self.height))
        self.scale_down_image()

        #ultimately, what we need is:        
        self.translate_x = None
        self.translate_y = None
        self.scale_factor= None
        self.angle = None
        
        self.left_eye_image_coordinates = self.get_image_coordinates(left_eye_landmark)
        self.right_eye_image_coordinates = self.get_image_coordinates(right_eye_andmark)
        try:
            self.left_eye_x, self.left_eye_y = self.left_eye_image_coordinates[0],self.left_eye_image_coordinates[1]
            self.right_eye_x, self.right_eye_y = self.right_eye_image_coordinates[0],self.right_eye_image_coordinates[1]
            self.y_difference = self.right_eye_y - self.left_eye_y
            self.x_difference = self.right_eye_x - self.left_eye_x
        except Exception as error:
            self.x_difference = None
            self.y_difference = None
            self.right_eye_x = None
            self.left_eye_x = None
            
            # Handle error logic within the align_image_to_base_image class
            # Don't mask errors
            print(str(error))
       

    def get_alignment_info(self, ultimate_base_image):   #eyePoint = (BaseImage.LeftEyeX,BaseImage.LeftEyeY)
        # this is because we just want to do a mock alignment to get the info, not a final one, we want to revert it back at the end.
        original = self.cvimage 
        old_x_difference = self.x_difference
        self.ultimate_base_image_height,self.ultimate_base_image_width = ultimate_base_image.cvimage.shape[:2]
        self.ultimate_dimensions = (self.ultimate_base_image_width, self.ultimate_base_image_height)
        self.ultimate_scale_factor = ultimate_base_image.x_difference / self.x_difference
        self.exact_x_difference = self.x_difference * self.ultimate_scale_factor
        center = (self.left_eye_x, self.left_eye_y)

        # I was looking for a way to scale around an image for so long, it was so simple
        matrix = cv.getRotationMatrix2D((0,0), 0, self.ultimate_scale_factor)

        # the final one in warp affine is the image dimensions
        self.cvimage = cv.warpAffine(self.cvimage, matrix, ultimate_base_image.dimensions)
 
        self.ultimate_translate_x = ultimate_base_image.left_eye_x - self.left_eye_x
        self.ultimate_translate_y = ultimate_base_image.left_eye_y - self.left_eye_y

        eye_point = (self.left_eye_x, self.left_eye_y)

        # tangent formula right triangle
        self.ultimate_angle = np.rad2deg(np.arctan( (self.right_eye_y - ultimate_base_image.right_eye_y) / self.exact_x_difference)) 
        
        # I'm trying out ultimate base image as the denominator because it should be the same?
        self.reset()
