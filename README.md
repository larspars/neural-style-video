# neural-style-video
Application of Gatys' [neural style transfer algorithm](http://arxiv.org/abs/1508.06576) to video.

Much of the following is lifted from Gene Kogans [instructions](https://gist.github.com/genekogan/d61c8010d470e1dbe15d).

1) Extract frames from video using ffmpeg

    ffmpeg -i myMovie.mp4 -r 12 -f image2 image-%5d.jpg
    ffmpeg -i myMovie.mp4 rawaudio.wav
    
This will extract frames at 12 fps.

2) Install and run jcjohnsons implementation of the [neural style transfer algorithm](https://github.com/jcjohnson/neural-style), with dependencies.

3) Run the neural style transfer algorithm.

    th neural_style.lua -style_image myStyle.jpg -content_image image-00001.jpg -output_image generated-00001.jpg
    
4) Calculate optical flow, morph and blend in the stylized image.

    python opticalflow.py --input_1 image-00001.jpg --input_1_styled generated-00001.jpg --input_2 image-00002.jpg --output blended-00001.jpg --alpha 0.05 --flowblend False

(The flowblend option will set scale the opacity according to the amount of motion - I didn't get good results with this, so you should probably set it to false)
    
5) When all frames are blended, you can merge them back into a video by calling

    ffmpeg -framerate 12 -i generated-%05d.png -i rawaudio.wav -c:v libx264 -preset veryslow -qp 0 -pix_fmt yuv420p myMovie.mp4
    
License: MIT

