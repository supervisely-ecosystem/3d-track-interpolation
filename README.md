<div align="center" markdown> 

<img src="https://github.com/supervisely-ecosystem/3d-track-interpolation/assets/119248312/08eed5f6-0775-4380-9233-3fc9b2752533" />

# 3D BBox Interpolation
  
<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Track-Examples">Track Examples</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/3d-track-interpolation)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/3d-track-interpolation)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/3d-track-interpolation)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/3d-track-interpolation)](https://supervise.ly)

</div>

# Overview 

This app is used to track the movement and position of 3D bounding boxes within a point cloud. The application uses spline interpolation to estimate the position of an object between two known data points in order to accurately track its movement over time.

# How To Run

1. Start the application from Ecosystem.

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/mbptrack3d/supervisely_integration/serve" src="https://github.com/supervisely-ecosystem/3d-track-interpolation/assets/115161827/ed3adf13-b716-47ed-a1e3-9e034312c819" width="1000px" style='padding-bottom: 20px'/> 

2. This app can be run only on your own agent. Watch [video](https://www.youtube.com/watch?v=aO7Zc4kTrVg) to learn how to connect your computer to Supervisely.

3. Open the `3D Episodes Labeling Toolbox` on the project you want to work with.

4. Create classes with `Cuboid` shapes and then draw figures on the several frames.

5. Choose the start frame (or range of frames via the `Select` tool), in track settings select running **3D BBox Interpolation** app, direction, and number of frames

6. Click `Interpolate` button. When a figure on the starting frame is selected, tracking begins for that figure. Be aware that interpolating will not work if some class has only a figure in the start frame and none in the tracking direction.

<a data-key="sly-embeded-video-link" href="https://youtu.be/ked5SFLjfRU" data-video-code="ked5SFLjfRU"> <img src="https://github.com/supervisely-ecosystem/3d-track-interpolation/assets/119248312/b5490e95-580f-46a4-acb1-b60339eb86b0" alt="SLY_EMBEDED_VIDEO_LINK"  style="max-width:100%;"> </a> 

# Track Examples

<div align="center">

<img src="https://user-images.githubusercontent.com/87002239/231757938-730b1deb-5887-47d7-a299-616411ffefa3.png" />

</div>

Frames #18, #25, #30 contains figures of 3 different objects.

| Objects   | Frames with figure | Frame range    | Track result                                                                  |
| --------- | ------------------ | -------------- | ----------------------------------------------------------------------------- |
| Object #1 | 18, 25, 30         | 18-27, forward | New figures will appear at frames 18-27                                       |
| Object #2 | 18, 25             | 18-27, forward | New figures will appear at frames 18-25                                       |
| Object #3 | 18                 | 18-27, forward | Tracking will fail because object #3 lacks sufficient data for interpolation. |


# Result
   
https://user-images.githubusercontent.com/119248312/282230125-c6496e5d-685b-4cbc-be14-f674aeb3250f.mp4

