# ConvertMediaToPose
This project focuses on running the mediapipe ML model and transforming its output into the original output of the openpose ML model

## Run with Docker

- Clone this repository
- Build the Docker image from the repository's root path: 
```
docker build -t <image-name> .
```
- Create the container from the repository's root path:
```
docker run -v <frames path on host>:/train_img -v <output path on host>:/output_mediapipe --gpus all --rm -it <image-name>
```
- Example of use:
```
docker run -v /homeLocal-projects/captarlibras_finep/analucia/mediapipe/train_img:/train_img -v ./output_mediapipe:/output_mediapipe --gpus all --rm -it captar-libras-mediapipe
```
- Run in your container:
```
python3 convert_media_to_pose.py --frames_dir /train_img --output_dir /output_mediapipe
```
