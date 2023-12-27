
## Daily Picture Aligner
Have you wanted to create one of those daily picture videos, but you didn't want to align each picture? Well, now you don't have to. Align ~~hundreds~~ _thousands_ of pictures automatically.

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
The project was birthed from [Hugo Cornellier's video taking a picture everyday from age 12 until he was married](https://www.youtube.com/watch?v=65nfbW-27ps)

#### !!Current State!!:
- *In this version, alignments are working well and accurately, even when images are scaled from larger dimenstions (e.g. 3000x3000) to smaller dimensions (1920x1080). This is iPhone -> Mobile Webcam*

## Running:
1. Put some images into the DailyPhotos Folder.
2. For every unique resolution, choose 1 photo and copy it into the BaseImage folder (i.e you have images that are either 1920x1080, 1280x720, 3000x2000, choose 1 of each type and put it into BaseImages folder)
3. Run main.py!
4. Check the output! If there's some funky stuff, see known issues, and check the error.txt file.
5. Make an image sequence video or a gif!

## How it works (Overview)

### 1. Preparation:
  - Photos are placed in the "DailyPhotos" folder. The face that is to be aligned should be in the center of the image.
  - ***<ins>One</ins>*** BaseImage is  provided in the base images folder. This image should have desired face position and scale, as all other images will be aligned to this image.

### 2. Script:
   ### Alignment Process:
  - The script creates a "BaseImage" object instance for the image in the "BaseImage" folder.   
  - Each image is then aligned to the BaseImage using the calculated transformations (scale, translate, rotate).
  - The image is then written to the output path with a suffix and affix. 


## Known Issues:
- Sometimes, there are just some images that simply don't like getting aligned properly. I found that about 2% of my photos (out of ~300) do  this for some reason. Just delete them and keep it pushing honestly.
- The current classes.py and main.py likely has some unused code. Previous code regarding the multiple alignments hasn't been cleaned yet.

  
## Other files:
- #### webcam_facemesh.py:
- This file was made to see the transformations live as I was working on functions. It made it easier, and it was kind of cool to see.
- ### slideshow.py:
- This file was made to see the finished product of the AlignedPhotos without having to go onto a gifmaker site or some opensource gif maker. Quick and easy to see how it looks.
- Paste in the desired path to photos, then enter the desired waitkey (delay), shorter is faster.

## Contributing:
- Woa, you want to contribute, eh? Thanks, that means a lot! Feel free to write a pull request or reach out to me for any questions or ideas!
- A few ideas I want to implement that I'm not sure how to in case you'd like to implement them!
   1. Basic GUI to make this program more accessible to people who don't know how to run python scripts
   2. In depth error messages for the error.txt file.
  
## Final Thoughts:
- If you found this project useful, or interesting, please reach out to me!! This project has been my passion project and it's been a direct representation of my coding growth over the years. I'd love to see how you'd like to use it.
- If you *really* found this project helpful, if you'd like to support me and this project, my CashApp is $ANoahBuchanan!