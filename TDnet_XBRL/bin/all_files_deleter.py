import files_deleter as rmv

def delete_all_files(folder_path):
    rmv.delete_zip_files(folder_path)
    rmv.delete_xml_files(folder_path)
    rmv.delete_xsd_files(folder_path)
    rmv.delete_txt_files(folder_path)
    rmv.delete_htm_files(folder_path)

if __name__ == '__main__':
    folder_path = r'C:\Users\SONY\PycharmProjects\pythonProject\TDnet_XBRL\zip_files\2780'
    delete_all_files(folder_path)
