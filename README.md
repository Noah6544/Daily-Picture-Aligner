# Development Branch

#### Everything here is in an incomplete state. RUN AT YOUR OWN RISK!

    This project is nearning the finish line after 2 years, now that its using MediaPipe FaceMesh .

## Documentation
### "Transformation_FaceMesh_Wip"   

    
- This is the going to be the main application for the program. Currently, I have this file as the updated version which is using MediaPipes "FaceMesh" to detect 468 individual points. 

      This file uses MediaPipe's FaceMesh solution for eye coordinates (more accurate).
 
      Currently working on updating this to extract these points for each image.

- The difference between this file and "Transformation WIP updated.py" is that this file uses MediaPipes FaceMesh to gather the points which is much more accurate (WIP), as apposed to the rough approximations of MediaPipes FaceDetection.

### Transformation_FaceDetection_Old
    This file uses MediaPipe's FaceDetection solution for eye coordinates (inaccurate).
- This file works in that it translates the images, except it is largely inaccurate, and the math that moves the images is likely wrong. This is the precursor and more crude version of the above file.


### heic_to_jpg
    Currently broken as CV doesn't recognize "converted" images. DO NOT USE.
- As the name suggests, this is  a quick script to convert between the iphone file type in the case that the users is taking the daily pictures with their phone, as I am. 

### webcam_facemesh.py

- This is an interesting script which uses the computer's webcame to display the facemesh on the subjects face.
- This script was a proof of concept and mainly taken from MediaPipes documentation page to see how much more accurate the facemesh model was.