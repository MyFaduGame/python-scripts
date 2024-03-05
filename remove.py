from PIL import Image
from pathlib import Path
from rembg import remove,new_session
import cv2

def remove_byte(input_path:str,output_path:str):
    
    try:
        with open(input_path,'rb') as i:
            with open(output_path,'wb') as o:
                input = i.read()
                output = remove(input)
                o.write(output)

    except Exception as e:
        print(e)
        return False    
    
    return True

def remove_direct(input_path:str,output_path:str):

    try:
        input = Image.open(input_path)
        output = remove(input)
        output.save(output_path)

    except Exception as e:
        print(e)
        return False

    return True

def remove_cv2(input_path:str,output_path:str):

    try:
        input = cv2.imread(input_path)
        output = remove(input)
        cv2.imwrite(output_path, output)

    except Exception as e:
        print(e)
        return False

    return True

def remove_path(input_folder:str):

    try:
        session = new_session()
        for file in Path(input_folder).glob('*.png'):
            input_path = str(file)
            output_path = str(file.parent / (file.stem + ".out.png"))

            with open(input_path, 'rb') as i:
                with open(output_path, 'wb') as o:
                    input = i.read()
                    output = remove(input, session=session)
                    o.write(output)
    except Exception as e:
        print(e)
        return False
    
    return True