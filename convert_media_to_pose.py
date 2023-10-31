import mapping

import json
import os
import argparse
from pathlib import Path
import cv2

def capture_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames_dir", type=str, help="Image frames directory")
    parser.add_argument("--output_dir", type=str, help="Output json directory")

    args = parser.parse_args()
    return args

def clean_output_dir(output_dir):
    # Verifica se o diretório existe
    if os.path.exists(output_dir):
        # Lista todos os arquivos e subdiretórios no diretório
        for item in os.listdir(output_dir):
            item_path = os.path.join(output_dir, item)

            # Verifica se o item é um arquivo
            if os.path.isfile(item_path):
                # Remove o arquivo
                os.remove(item_path)

try:
    args = capture_args()
    os.chdir(os.getcwd())
    files = sorted(os.listdir(args.frames_dir))

    clean_output_dir(args.output_dir)
        
    pose_keypoints_2d = []
    face_keypoints_2d  = []
    hand_left_keypoints_2d = []
    hand_right_keypoints_2d = []

    print("=========================== RUN MODEL ===========================")

    for file in files:
        img = cv2.imread(args.frames_dir + '/' + file)

        # Run MediaPipe Holistic and draw pose landmarks.
        with mapping.mp_holistic.Holistic(static_image_mode=False, 
                                            min_detection_confidence=mapping.CONFIANCE_INDEX, min_tracking_confidence=mapping.CONFIANCE_INDEX,
                                            model_complexity=2, refine_face_landmarks=True, smooth_landmarks=True) as holistic:  
            # Converta a imagem BGR em RGB e processe-a com MediaPipe Pose.
            results = holistic.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) # tem que transformar em RGB, se não da erro.
            print(file)
            img_hight, img_width = img.shape[:2]
            if results:

                pose_keypoints_2d = mapping.map_pose(results, img_hight, img_width) if results.pose_landmarks else pose_keypoints_2d
                face_keypoints_2d = mapping.map_face(results, img_hight, img_width) if results.face_landmarks else face_keypoints_2d
                hand_left_keypoints_2d = mapping.map_left_hand(results, img_hight, img_width) if results.left_hand_landmarks else hand_left_keypoints_2d
                hand_right_keypoints_2d = mapping.map_right_hand(results, img_hight, img_width) if results.right_hand_landmarks else hand_right_keypoints_2d

                output = {
                    'version': 1.3,
                    'people': [
                        {
                            'person_id':[-1],
                            'pose_keypoints_2d': pose_keypoints_2d ,
                            'face_keypoints_2d': face_keypoints_2d,
                            'hand_left_keypoints_2d': hand_left_keypoints_2d,
                            'hand_right_keypoints_2d': hand_right_keypoints_2d,
                            'pose_keypoints_3d':[],
                            'face_keypoints_3d':[],
                            'hand_left_keypoints_3d':[],
                            'hand_right_keypoints_3d':[]
                        }
                    ]
                }

                file_name = file.split('.')[0]

                with open(args.output_dir + '/' + file_name + '.json', 'w') as file:
                    json.dump(output, file)
                        
            else:
                print('Fail')
        
    print("=========================== FINISH ===========================")
            
except:
    print('No arguments provided')
