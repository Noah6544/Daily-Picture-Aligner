## Daily Picture Aligner
Have you wanted to create one of those daily picture videos, but you didn't want to align each picture? Well, now you don't have to. Align ~~hundreds~~ _thousands_ of picture automatically.

### Description
The project was birthed from [Hugo Cornellier's video taking a picture everyday from age 12 until he was married](https://www.youtube.com/watch?v=65nfbW-27ps)


#### Current State:
- *the current state is just a working build of the 1st alignment: read below. Functional, but incomplete.*
 
## How it works (Overview)
### 1. Preperation:
  - Photos are placed in the "DailyPhotos" folder. The face that is to be aligned should be in the center of the image.
  - "Base Images" are provided in the base images folder. These are images that have ideal face position and scale, all other images of the same resolution (i.e: 1920x1080, 1280x720, etc.) will be aligned to this image. 
### 2. Script:
   ### First Alignment:
  - The script creates a "BaseImage" object instance for every image in the "BaseImage" folder. Each BaseImage is then "aligned" to the BaseImage that has the smallest resolution out of all other BaseImages. The smallest BaseImage is reffered to as the "UltimateBaseImage" within the code. The alignment isn't actually done, instead, the data for each transformation is stored for later. Why?
  - Each image inside "DailyPhotos" gets aligned to is correspoinding BaseImage (one that has the same resolution).
  ### Second Alignment:
  
  - Each image is *then* aligned to the UltimateBaseImage using the transformations stored within it's corresponding BaseImage's attributes.
  - The image is the written to the output path with a suffix and affix. 

## Reasoning:
### Problem:
- I found that having images taken on modern phones are quite large (3000x2000+), and aligning these large photos down to smaller webcam photos seems to introduce a lot of errors and variability, making the final video less stable.
#### Solution:
- Instead of bruteforcing alignment from all images to 1 selected image, instead we have multiple BaseImages which let all images with the same resolution to be aligned to each other. Then *all* these images are aligned with *the same* transformations as their base image, this will mean that if there are errors from the corresponding BaseImage -> UltimateBaseImage that they will be for all other images, so the misalignment will only seem that way when switching from different resolutioned photos!


### Known Issues.
- Currently, in this working mode, the second alignment is not working. I have commented it out in main.py within the if statement. The arctan calculation keeps throwing extremely high values for the angle rotation when I try to do the 2nd alignemnt for some reason. For this reason, the script only works with the first alignment, so all images with like resolution will be aligned to each other
- Sometimes, there are just some images that simply don't like getting aligned properly. I found that about 2% of my photos (out of ~300) do  this for some reason. Just delete them and keep it pushing honestly.
