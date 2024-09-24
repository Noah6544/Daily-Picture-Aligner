
## Daily Picture Aligner
Have you wanted to create one of those daily picture videos, but you didn't want to align each picture? Well, now you don't have to. Align ~~hundreds~~ _thousands_ of pictures automatically. No sifting through documentation and no coding knowledge necessary, simply run one script and enjoy your aligned photos.

## Demos: 
 
<div align=center>
  
### Personal Daily Photos:
![Personal Daily Demo](https://github.com/Noah6544/Daily-Picture-Aligner/blob/master/Demos/RecentDailyGif.gif)

### Unaligned Random Faces:
![Unaligned Random Faces](https://github.com/Noah6544/Daily-Picture-Aligner/blob/master/Demos/UnalignedRandomFaces.gif)


### Aligned Random Faces: 
![Aligned Random Faces](https://github.com/Noah6544/Daily-Picture-Aligner/blob/master/Demos/AlignedRandomFaces.gif)

</div>

## Description
The project was birthed from [Hugo Cornellier's video taking a picture everyday from age 12 until he was married.](https://www.youtube.com/watch?v=65nfbW-27ps) Hugo manually aligned thousands of pictures by hand. While he had the precision he sought, he lost  valuable time (not to say his finished product wasn't worth it, it is incredible!). This project automates the countless hours you will otherwise spend editing each individual photo. While another solution exists: Matthew's <a href="https://github.com/matthewearl/photo-a-day-aligner">'photo a day aligner,'</a> I feel this project is more user friendly (less complex and versatile), as non-programmers can quickly get it up and running by dragging some photos in a few folders, and running a script. Plus, there's no dealing with dlib, as its installation is <ins>**UNFATHOMABLY**</ins> troublesome for myself and others, but I'll digress from the bad memories.

## Running:
#### *I'm working on implementing a functional executable soon for non-programmers.*
1. Install python ([a version supported by mediapipe](https://ai.google.dev/edge/mediapipe/solutions/setup_python) and 64bit) then requirements.txt.
2. Put some images into the DailyPhotos Folder.
3. Choose 1 photo where the face is ideal (scale, position, rotation) and copy it into the BaseImage folder. This image should be the smallest resolution you have, as images being scaled down appears better than images scaled up (e.g. if you have 2 3000x3000 pictures, 5 pictures 1920x1080 pictures, and 3 pictures 1280x720, choose one that is 1280x720).
4. Run main.py! Alternatively, if you're not as familiar with python, skip to #7.
5. Quickly check the output using slideshow.py/slideshow.exe in 'misc' folder. If there's some funky stuff, see known issues, and check the error.txt file.
6. Make an image sequence video or a gif!
7. Check out [my quick guide video](https://www.youtube.com/watch?v=_ow6GLv7VSA&) on how to run this project if you need help or want to see a demo.

## How it works (Overview)

### 1. Preparation: 
  - Photos are placed in the "DailyPhotos" folder. The face that is to be aligned should be in the center of the image.
  - ***<ins>One</ins>*** BaseImage is provided in the base images folder. This image should have desired face position and scale, as all other images will be aligned to this image.
  - Delete all "DELETETHIS.txt" files. They are simply placeholders so folders are created for you.

### 2. Script:
   ### Alignment Process:
  - The script creates a "BaseImage" object instance for the image in the "BaseImage" folder.   
  - Each image is then aligned to the BaseImage using the calculated transformations (scale, translate, rotate).
  - The image is then written to the output path with a suffix and affix. 


## Known Issues:
- Sometimes, there are just some images that simply don't like getting aligned properly. I found that about 2% of my photos (out of ~300) do  this for some reason. Just delete them and keep it pushing honestly.
- Similarly, the script will sometimes lock onto another face in the image, this happens sometimes, if it does, delete that image as it will continually make the same mistake over and over. But if your face is in the center and most prominent, it seems to do just fine. I'm working on implementing a searching method to only work on the desired face as I enjoy taking pictures spontaneously with friends and siblings and it's unfortunate to have to omit those photos.
- The current classes.py and main.py likely has some unused code. Previous code regarding the multiple alignments hasn't been cleaned yet.

  
## Other files:
- #### webcam_facemesh.py:
- This script was made to see the transformations live as I was working on functions. It made it easier, and it was kind of cool to see.
- ### slideshow.py:
- This script was made to see the finished product of the AlignedPhotos without having to go onto a gifmaker site or some opensource gif maker. Quick and easy to see how it looks.
- Paste in the desired path to photos, then enter the desired waitkey (delay), shorter is faster.

## Contributing:
- Woa, you want to contribute, eh? Thanks, that means a lot! Feel free to write a pull request or reach out to me for any questions or ideas!
- A few ideas I want to implement that I'm not sure how to in case you'd like to implement them!
   1. Basic GUI to make this program more accessible to people who don't know how to run python scripts
   2. Handling multiple faces by aligning to the same face everytime (to avoid getting into ML and face recognition which might make the 'bundle size' a lot larger, I was thinking of implementing a basic crop to the center of each image, extrapolating the transformation data, then 'uncropping' in the finished file. I think this would be efficient and 95% effective).
   3. In depth error messages for the error.txt file.
   4. I tried to create an executable using pyinstaller, but I can't get the dependencies to work properly, I think that's a good first issue on this project!
  
## Final Thoughts:
- If you found this project useful, or interesting, please reach out to me!! This project has been my passion project and it's been a direct representation of my coding growth over the years. I'd love to see how you'd like to use it.
- If you *really* found this project helpful, if you'd like to support me and this project, my CashApp is $NoahCutz, or you can 'Buy Me A Coffee' ;)

<p align='center'><a href="https://www.buymeacoffee.com/NoahBuchanan" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png" alt="Buy Me A Coffee" width="150" ></a></p>
