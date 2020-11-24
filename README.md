# Daily-Picture-Aligner
This program is intended to eventually be able to take all photos in a folder and align them automatically based on a given feature (eye, hair, eyebrow, etc.)
I plan for it to use opencv2 to align pictures based on a given feature, but (as of 10-8-2020) I haven't learned any opencv2 besides basic things (imread, imshow, waitkey, etc.)
# Current Version (Second)
The only thing that changed with this commit is that pictures display in color by default, forogt to set the flag as 1 instead of 0 which is color and grayscale respectively. 
# Issues
- There's a problem where files aren't either being added to the list or aren't being displayed, with my directory of images about 80 of the 200+ images aren't being displayed. 
` Files aren't displayed in order either, which deafeats the purpose of what I'm trying to make.
### ToDo
- Learn opencv drawing and identifying specific features (I don't know any of the actual termonoligy)
- Have adjusted pictures be written to a new directory.
- Possibly choices to be aligned at different features (hair, eyebrows, leg, torso, etc.).
- Dislay files by creation date
-- Possible create and option for in which order they'll be displayed (oldest, latest)


### Archived commits
# First Commit
Completed:
- File managment, gathering pictures from a given directory and taking all photos from it that aren't curropted (0 bytes in size). Opencv2 can display all of the pictures without any alignment, just raw pictures (not raw as in file type).
- Essentially it's a picture slide player that slides pictures at the speed you want
