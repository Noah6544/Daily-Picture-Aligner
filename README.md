# Daily-Picture-Aligner
*looking for a more updated, working version? Checkout the development branch! It's not ready for user input, so you'll have to do some modification of the python file itself, but you can align photos there!*
<br><br>
 [Demo](https://github.com/Noah6544/Daily-Picture-Aligner/blob/master/choppedprephone.gif)

This program is intended to take all photos in a folder and align them automatically based on the eye coordinates of a set base image.
This project is using opencv to handle opening, displaying, and translating images. MediaPipe provides 468 facial landmarks to extract and calculate with.

#### Do not run any files called "Transformation" or the "heic_to_jpg" as they are both WIP and not complete.

# Inspiration
- I wanted to make this after manually aligning the first 60 pictures of my picture-every-day project. It took hours in total and I hope this can save me and lots of people time. 
- I want to make a tutorial which will have an easier to use executable file for people on YouTube who might be wanting to do a similar thing without getting discouraged with all the editing programs or github pages.
- Resume project and something that could give me ego points if I post to reddit
- ## As with all personal projects, I hope to learn more about coding, github, and the entire process as a whole; I want to increase my experience.

# ToDo
- Have adjusted pictures be written to a new directory.
- Possibly choices to be aligned at different features (hair, eyebrows, leg, torso, etc.).
- Possibly create and option for in which order they'll be displayed (oldest, latest).
- Possible create a GUI version

# Contributions
- I greatly appreciate your interest in this project. Feel free to play around with it and fork to experiment.
- However, this project is a real learning process for me so until I get a releasable version I won't be merging any pull requests because this is a fairly simple project I think an expert could do in a few days.


## Documentation
### "Transformation_FaceMesh_Wip"   

### INCOMPLETE
    
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





