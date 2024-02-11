import cv2
import face_recognition
import os

def process_image(image_path):

    # Load the reference image
    reference_image_path = image_path
    reference_image = face_recognition.load_image_file(reference_image_path)
    reference_face_encoding = face_recognition.face_encodings(reference_image)[0]

    # Load the video file
    video_path = 'IMG_3286.mp4'
    cap = cv2.VideoCapture(video_path)

    # Create an output directory to save cropped faces
    output_directory = 'output_faces'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)


    # Function to crop and save face images
    def crop_and_save_faces(frame, face_locations, output_directory, frame_count):
        for i, face_location in enumerate(face_locations):
            top, right, bottom, left = face_location
            face_image = frame[top:bottom, left:right]
            cv2.imwrite(os.path.join(output_directory, f"face_{frame_count}_{i}.jpg"), face_image)


    # Function to compare faces with the reference image
    def compare_faces_with_reference(output_directory, reference_face_encoding):
        for filename in os.listdir(output_directory):
            if filename.endswith(".jpg"):
                face_image_path = os.path.join(output_directory, filename)
                face_image = face_recognition.load_image_file(face_image_path)
                face_encoding = face_recognition.face_encodings(face_image)

                # Check if any face in the current image matches the reference face
                if len(face_encoding) > 0 and face_recognition.compare_faces([reference_face_encoding], face_encoding[0])[
                    0]:
                    print(f"Match found! Face in {filename} matches the reference face.")
                else:
                    print(f"No match found for {filename}.")

    # Define the skip factor (e.g., process every 5th frame)
    skip_factor = 5

    # Process the frames
    frame_count = 1
    while True:
        # Read the current frame
        ret, frame = cap.read()
        if not ret:
            break  # Break the loop if no frames are left

        # Skip frames based on the skip factor
        if frame_count % skip_factor == 0:
            # Find face locations in the current frame
            face_locations = face_recognition.face_locations(frame)

            # Crop and save faces
            crop_and_save_faces(frame, face_locations, output_directory, frame_count)

        frame_count += 1

    # Compare faces in the output directory with the reference image after processing all frames
    compare_faces_with_reference(output_directory, reference_face_encoding)

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

    merged_video_path = 'merged_video.mp4'  # Example path to the merged video
    return merged_video_path
