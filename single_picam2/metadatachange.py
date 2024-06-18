import piexif
import os

# image1="/home/jimmyzhang/Desktop/images/test1.jpg"
# exif_dict=piexif.load(image1)
# print (exif_dict)

# thumbnail = exif_dict.pop('thumbnail')

# for ifd in exif_dict:
#     # print (f'{ifd:}')
#     print (ifd)
#     for tag in exif_dict[ifd]:
#         print (tag)
#         tag_name = piexif.TAGS[ifd][tag]["name"]
#         #print (tag_name)
#         tag_value=exif_dict[ifd][tag]
#         #print (tag_value)
#         if isinstance(tag_value,bytes):
#             tag_value = tag_value [:10]
#         print (f'\t{tag_name:25}:{tag_value}')

# print (exif_dict['Exif'][33434])
# #(25,10) means 25/10=2.5mm focal length
# exif_dict['Exif'][piexif.ExifIFD.FocalLength]=(25,10)
# print (exif_dict['Exif'][37386])

# exif_bytes = piexif.dump(exif_dict)
# piexif.insert(exif_bytes,image1,'/home/jimmyzhang/Desktop/images/copy1.jpg')


def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Folder '{path}' created.")
    else:
        print(f"Folder '{path}' already exists.")

counter=1
image_import_directory = '/home/jimmyzhang/Desktop/images'
create_folder_if_not_exists('/home/jimmyzhang/Desktop/images_editted')
image_save_directory = '/home/jimmyzhang/Desktop/images_editted'
for filename in os.listdir(image_import_directory):
    img_import_path = os.path.join (image_import_directory, filename)
    exif_dict=piexif.load(img_import_path)
    exif_dict['Exif'][piexif.ExifIFD.FocalLength]=(275,100)
    exif_dict['Exif'][piexif.ExifIFD.FocalLengthIn35mmFilm]=(16,1)
    exif_bytes = piexif.dump (exif_dict)
    editted_filename=f"image{counter}.jpg"
    counter +=1
    img_save_path = os.path.join (image_save_directory, editted_filename)
    piexif.insert(exif_bytes, img_import_path, img_save_path) 

