import cv2
import numpy as np

def main():
    imagem1 = cv2.imread(f'debug/reduced_video_frames/reduced_video_frames_01-47-30_695.jpg')
    imagem2 = cv2.imread(f'debug/reduced_video_frames/reduced_video_frames_01-47-44_495.jpg')

    is_frame_similar(imagem1, imagem2)

def is_frame_similar(frame1, frame2, threshold=20000000): # 20.000.000 passou disso quer dizer que as fotos são diferentes
    # Calcule a diferença absoluta entre os dois quadros
    diff = cv2.absdiff(frame1, frame2)
    
    #resumir as diferenças
    sum_diff = np.sum(diff)
    
    # Se a soma das diferenças for menor que o limite, os quadros são semelhantes
    print("sum_diff: ", sum_diff)

if __name__ == "__main__":
    main()
