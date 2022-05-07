from utils.image_utils import image_saver

is_vehicle_detected = [0]
current_frame_number_list = [0]
current_frame_number_list_2 = [0]
bottom_position_of_detected_vehicle = [0]


def predict_speed(
    top,
    bottom,
    right,
    left,
    current_frame_number,
    crop_img,
    roi_position,
    ):
    speed = 'n.a.' 
    direction = 'n.a.' 
    scale_constant = 1  
    isInROI = True  
    update_csv = False

    if bottom < 250:
        scale_constant = 1  
    elif bottom > 250 and bottom < 320:
        scale_constant = 2  
    else:
        isInROI = False

    if len(bottom_position_of_detected_vehicle) != 0 and bottom \
        - bottom_position_of_detected_vehicle[0] > 0 and 195 \
        < bottom_position_of_detected_vehicle[0] \
        and bottom_position_of_detected_vehicle[0] < 240 \
        and roi_position < bottom+100 and (current_frame_number - current_frame_number_list_2[0])>24:
        is_vehicle_detected.insert(0, 1)
        update_csv = True
        image_saver.save_image(crop_img)  
        current_frame_number_list_2.insert(0, current_frame_number)
  
    if bottom > bottom_position_of_detected_vehicle[0]:
        direction = 'down'
    else:
        direction = 'up'

    if isInROI:
        pixel_length = bottom - bottom_position_of_detected_vehicle[0]
        scale_real_length = pixel_length * 44  
        total_time_passed = current_frame_number - current_frame_number_list[0]
        scale_real_time_passed = total_time_passed * 24  
        if scale_real_time_passed != 0:
            speed = scale_real_length / scale_real_time_passed / scale_constant  
            speed = speed / 6 * 40  
            current_frame_number_list.insert(0, current_frame_number)
            bottom_position_of_detected_vehicle.insert(0, bottom)
    return (direction, speed, is_vehicle_detected, update_csv)
