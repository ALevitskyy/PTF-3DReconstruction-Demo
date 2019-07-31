# Instruction

1. Download assets from https://al-deeplearn.s3.amazonaws.com/assets.zip and unpack
The asset folder include:
 - aca95_texture_new0.png - texture image, can use different one
 - alphapose-results-forvis-tracked.json output got from running HMMR https://github.com/akanazawa/human_dynamics on video. The output is keypoints after Alphapose tracked using Hungarian algorithm
 - basicmodel_m_lbs_10_207_0_v1.0.0.pkl - sample SMPL model
 - hmmr_output.pkl - output of HMMR, pickle contains coordinates of all vertices as well as other SMPL parameters for each frame
 - homo.pkl - Pickle of Homography matrices obtained by running poxyu`s notebook https://github.com/poxyu/punch-to-face-tech/blob/master/scripts/baseline_pipeline_tutorial.ipynb - one matrix for each frame

2. Create rendered_video and fighter1_model folders or whatever defined in config.py

3. Run python3 generate_assets.py, this will create obj files one for each frame in fighter1_model folder or whatever defined in config.py. Also positions.pkl is created, which contains 2D coordinate of fighter on canvas

4. Open Blender, set up lighting an run the following code in Blender console:

```
filename = "/Users/andriylevitskyy/Desktop/reconstruction/python_code/blender.py"
import sys
sys.path.append("/Users/andriylevitskyy/Desktop/reconstruction/python_code")
exec(compile(open(filename,"r+",encoding = "utf-8").read(), filename, 'exec'))
```

or whatever the relevant filenames

5. To make a video one can go to rendered_video folder (or whatever) and run:
```ffmpeg -framerate 24 -i %08d.png -pix_fmt yuv420p output.mp4```
